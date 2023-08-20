import sys
from board import Blackboard
from configuration import RoobokartLearnerConfiguration
from log import LoggerFactory
from training import train
from testing import test
import gym


modes = {
    'train': train,
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
        print('Have a nice day :)')
        exit(0)






### FROM HERE ##########

# Output for plot of rewards
'''


'''






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