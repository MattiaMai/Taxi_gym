import sys
from board import Blackboard
from configuration import RoobokartLearnerConfiguration
from log import LoggerFactory, Loggable







#è un algoritmo di Q-Learning: https://www.gocoder.one/blog/rl-tutorial-with-openai-gym/

#PACCHETTI DA IMPORTARE SCRITTI NEL README

"""Importo i pacchetti"""
import imageio # Salva i frame nel file video utilizzando imageio
import gym #lo utilizzo per creare l'envirmoent taxi
import numpy as np #lo utilizzo per la gestione dei vettori (in questo caso delle q-table )
import random #lo utilizzo per la scelta casuale dell'azione
from matplotlib import animation #lo tulizzo per generare l'animazione
import pickle #lo utilizzo per salvare il file h5

def learn():
    logger = Loggable('main')
    logger.info("This is a test")
    #todo
    pass

def test():
    #todo
    pass

modes = {
    'learn': learn,
    'test': test
}

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        blackboard = Blackboard()
        mode = sys.argv[1]
        configuration_filename = sys.argv[2]
        configuration = RoobokartLearnerConfiguration(configuration_filename)
        blackboard.put('configuration', configuration)
        environment = gym.make(configuration.get('env_name'),render_mode = configuration.get('render_mode'))
        blackboard.put('environment', environment)
        LoggerFactory.setup(configuration)
        modes[mode]()
        LoggerFactory.shutdown()
        print('End of Communication')
        exit(0)




'''
POTREI DIVIDERE IL MIO PROGRAMMA IN 2:
1) TRAINING
2) TEST
'''
#1)TRAINING
"""Inizializzare l'environment"""

# Print delle dimensioni dello stato e dello spazio delle azioni
print("State space: {}".format(env.observation_space))
print("Action space: {}".format(env.action_space))


"""Training dell'agente"""
q_table = np.zeros([env.observation_space.n, env.action_space.n])
'''
guarda: https://www.gymlibrary.dev/environments/toy_text/taxi/
per avere informazioni per quanto riguarda observationstape e actionspace di gym
'''

# Hyperparameters
"""
alpha = 0.1  # Learning rate
gamma = 1.0  # Discount rate
epsilon = 0.1  # Exploration rate
num_episodes = 10000  # Numero di episodi
"""
alpha = 0.8
gamma=0.5
epsilon=0.2
num_episodes=10000
num_epochs= 200000

# Output for plot of rewards
cum_rewards = np.zeros([num_episodes])

for episode in range(1, num_episodes + 1):
    # Reset environment
    state, info = env.reset()
    num_failed_dropoffs = 0
    done = False
    cum_reward = 0
    epoch = 0

    while not done and epoch<num_epochs:
        '''
        if random.uniform(0, 1) < epsilon:
        Questo tipo di costrutto viene spesso utilizzato nell'apprendimento per rinforzo (RL) per 
        l'esplorazione stocastica. Con una probabilità epsilon (exploration rate), viene effettuata una scelta
        casuale  piuttosto che seguire la politica appresa per consentire una maggiore esplorazione dell'ambiente.
        '''
        if random.uniform(0, 1) < epsilon:
            #random exploration
            action = env.action_space.sample()  # Sample random action (exploration)
        else:
            #exploitation ("sfruttamento")
            action = np.argmax(q_table[state])  # Select best known action (exploitation)

        #alla fine di questo if avro scelto la mia azione in base all'exploration rate
        next_state, reward, done, _, info = env.step(action)
        # dalla documentazione gym:
        # -1 per step unless other reward is triggered.
        # +20 delivering passenger.
        # -10 executing “pickup” and “drop-off” actions illegally.

        #next_state: Rappresenta lo stato successivo dopo aver eseguito l'azione nell'ambiente. Questo valore indica la situazione corrente dell'agente dopo aver effettuato l'azione.
        #reward: Indica la ricompensa ottenuta dall'agente per aver eseguito l'azione nello stato corrente. Questa ricompensa può essere positiva, negativa o nulla a seconda delle regole dell'ambiente e delle prestazioni dell'agente.
        #terminated (o done): È un valore booleano che indica se l'episodio è terminato o meno. Se terminated è True, significa che l'episodio è concluso e l'agente ha raggiunto uno stato terminale o ha soddisfatto una condizione di terminazione specifica. In caso contrario, terminated è False, indicando che l'episodio continua.
        #truncated (o _): È un valore booleano che può essere utilizzato per indicare se l'episodio è stato troncato o limitato in qualche modo. Questo può significare che l'episodio ha raggiunto un limite massimo di passi o che l'ambiente ha imposto una limitazione sulla durata dell'episodio.
        #info: Questo valore contiene informazioni aggiuntive sull'esito dell'azione, come dati diagnostici o dettagli specifici dell'ambiente. Tuttavia, questo valore è opzionale e può non essere restituito da tutte le implementazioni di un ambiente specifico.

        cum_reward += reward #mi serve solo per il grafico finale, ai fini dell'algoritmo è inutile

        old_q_value = q_table[state, action]
        next_max = np.max(q_table[next_state])

        new_q_value = (1 - alpha) * old_q_value + alpha * (reward + gamma * next_max)
        #Questa scrittura è del tutto equivalente al codice di q learning descritto nella tesi
        #new_q_value=old_q_value+ alpha*(reward + gamma* next_max - old_q_value)

        q_table[state, action] = new_q_value

        if reward == -10:
            num_failed_dropoffs += 1

        state = next_state
        epoch += 1
        #print(str(epoch))
        cum_rewards[episode - 1] = cum_reward #questa parte di codice mi serve per fare il plot finale dei rewards

    print(f"Episode #: {episode}")

    if episode % 100 == 0:
        print(f"Episode #: {episode}")

#alla fine del mio while, mi salvo la q_table finale del mio modello in un h5
file='taxi_brain.h5'
fw = open(file, 'wb')
pickle.dump(q_table, fw)
fw.close()
print(f"\nbrain saved as :{file}")

print("===Training completed.===\n")

#FINE FASE TRAINING (il programma training si conclude qui)

#faccio il plot della convergenza
# Plot reward convergence
plt.title("Cumulative reward per episode")
plt.xlabel("Episode")
plt.ylabel("Cumulative reward")
plt.plot(cum_rewards)
plt.savefig('cum_rewards.jpg', format='jpg', dpi=300) #salvo il grafico dei rewards in un'immagine
#plt.show() #commento plotshow per rendere tutto più server-frinedly




#2)TESTING
"""Test della performance della policy dopo la fase di training"""
total_failed_deliveries = 0
num_episodes = 1 #inserire un altro numero se si vogliono effettuare più di un test
store_gif = True #ponilo =False se non lo voglio salvare

for episode in range(1, num_episodes+1):
    # Initialize experience buffer
    my_env = env.reset()
    experience_buffer = []
    state = my_env[0]
    num_failed_deliveries =0
    cum_reward = 0
    done = False

    #carico il file h5 (il mio cervello)
    file='taxi_brain.h5'
    fr = open(file, 'rb')
    q_table_trained= pickle.load(fr)
    fr.close()
    print(f"brain {file} loaded \n")

    while not done:
        action = np.argmax(q_table_trained[state])
        state, reward, done, _, _ = env.step(action)
        # i reward presi dalla documentazione gym:
        # -1 per step unless other reward is triggered.
        # +20 delivering passenger.
        # -10 executing “pickup” and “drop-off” actions illegally.

        # next_state: Rappresenta lo stato successivo dopo aver eseguito l'azione nell'ambiente. Questo valore indica la situazione corrente dell'agente dopo aver effettuato l'azione.
        # reward: Indica la ricompensa ottenuta dall'agente per aver eseguito l'azione nello stato corrente. Questa ricompensa può essere positiva, negativa o nulla a seconda delle regole dell'ambiente e delle prestazioni dell'agente.
        # terminated (o done): È un valore booleano che indica se l'episodio è terminato o meno. Se terminated è True, significa che l'episodio è concluso e l'agente ha raggiunto uno stato terminale o ha soddisfatto una condizione di terminazione specifica. In caso contrario, terminated è False, indicando che l'episodio continua.
        # truncated: È un valore booleano che può essere utilizzato per indicare se l'episodio è stato troncato o limitato in qualche modo. Questo può significare che l'episodio ha raggiunto un limite massimo di passi o che l'ambiente ha imposto una limitazione sulla durata dell'episodio.
        # info: Questo valore contiene informazioni aggiuntive sull'esito dell'azione, come dati diagnostici o dettagli specifici dell'ambiente. Tuttavia, questo valore è opzionale e può non essere restituito da tutte le implementazioni di un ambiente specifico.

        cum_reward += reward

        if reward == -10:
            num_failed_deliveries += 1

        # Store rendered frame in animation dictionary
        experience_buffer.append({
            'frame': env.render(),
            'episode': episode,
            'state': state,
            'action': action,
            'reward': cum_reward
            }
        )


    total_failed_deliveries += num_failed_deliveries

    filename = "animation"

    if store_gif:
        filename = filename +" episodio "+ str(episode) + ".gif"
        store_episode_as_gif_and_video(filename,experience_buffer)



#Avvio dell'animazione
#run_animation(experience_buffer) #commenta l'animazione per rendere tutto più server-friendly

# Print dei risultati finali
print("\n")
print(f"Test results after {num_episodes} episodes:")
print(f"Mean # failed drop-offs per episode: {total_failed_deliveries / num_episodes}")

#Fine FASE TESTING