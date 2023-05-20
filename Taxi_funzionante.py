#è un algoritmo di Q-Learning: https://www.gocoder.one/blog/rl-tutorial-with-openai-gym/

#PACCHETTI DA IMPORTARE SCRITTI NEL README

"""Importo i pacchetti"""

import imageio
import gym
import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib import animation
import pickle

#definisco le dunzioni che mi permettono di fare il run dell'animazione e di salvarla in formato gif e mp4
#(Non sono fondamentali ai fini dello sviluppo del modello)
def run_animation(experience_buffer):
    """Funzione che lancia l'animazione"""
    time_lag = 0.4  # Delay (in s) between frames
    for experience in experience_buffer:
        # Plot del frame
        plt.imshow(experience['frame'])
        plt.axis('off')
        plt.show(block=False)
        # Pausa animazione
        plt.pause(time_lag)
        # Print console output
        print(f"Episode: {experience['episode']}/{experience_buffer[-1]['episode']}")
        print(f"Epoch: {experience['epoch']}/{experience_buffer[-1]['epoch']}")
        print(f"State: {experience['state']}")
        print(f"Action: {experience['action']}")
        print(f"Reward: {experience['reward']}")

    plt.close()


def store_episode_as_gif_and_video(experience_buffer):
    path = './'
    gifname = 'animation.gif'

    """Salvataggio aniazione come gif"""
    fps = 5   # imposto i frame per secondo
    dpi = 30  # imposto i dots per inch
    interval = 50  # intervallo tra i frames (in ms)

    frames = []
    for experience in experience_buffer:
        frames.append(experience['frame'])

    # Fix frame size
    plt.figure(figsize=(frames[0].shape[1] / dpi, frames[0].shape[0] / dpi), dpi=dpi)
    patch = plt.imshow(frames[0])
    plt.axis('off')

    # Generate animation
    def animate(i):
        patch.set_data(frames[i])

    anim = animation.FuncAnimation(plt.gcf(), animate, frames=len(frames), interval=interval)
    # Salvo l'output come gif
    # anim.save(path + filename, writer='imagemagick', fps=fps)
    # boh,mi da un warning dove dice che utilizza pillow al posto di pillow
    anim.save(path + gifname, writer='Pillow', fps=fps)


    """Salvataggio animazione come video"""
    # Specifica il nome del file video e il percorso di salvataggio
    video_path = 'video.mp4'
    # Specifica la durata di ciascun frame nel video (in secondi)
    frame_duration = 1
    # Salva i frame nel file video utilizzando imageio
    with imageio.get_writer(video_path, mode='I', fps=1 / frame_duration) as writer:
        for frame in frames:
            writer.append_data(frame)
    writer.close()


'''
POTREI DIVIDERE IL MIO PROGRAMMA IN 2:
1) TRAINING
2) TEST
'''
#1)TRAINING
"""Inizializzare l'environment"""
env = gym.make("Taxi-v3", render_mode="rgb_array")
state, _ = env.reset()

# Print delle dimensioni dello stato e dello spazio delle azioni
print("State space: {}".format(env.observation_space))
print("Action space: {}".format(env.action_space))


"""Training dell'agente"""
q_table = np.zeros([env.observation_space.n, env.action_space.n])

# Hyperparameters
alpha = 0.1  # Learning rate
gamma = 1.0  # Discount rate
epsilon = 0.1  # Exploration rate
num_episodes = 10000  # Numero di episodi

# Output for plots
cum_rewards = np.zeros([num_episodes])
total_epochs = np.zeros([num_episodes])

for episode in range(1, num_episodes + 1):
    # Reset environment
    state, info = env.reset()
    epoch = 0
    num_failed_dropoffs = 0
    done = False
    cum_reward = 0

    while not done:
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
            #selected exploratione
            action = np.argmax(q_table[state])  # Select best known action (exploitation)

        #alla fine di questo if avro scelto la mia azione in base all'exploration rate
        next_state, reward, done, _, info = env.step(action)

        cum_reward += reward

        old_q_value = q_table[state, action]
        next_max = np.max(q_table[next_state])

        new_q_value = (1 - alpha) * old_q_value + alpha * (reward + gamma * next_max)

        q_table[state, action] = new_q_value

        if reward == -10:
            num_failed_dropoffs += 1

        state = next_state
        epoch += 1

        total_epochs[episode - 1] = epoch
        cum_rewards[episode - 1] = cum_reward

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

#faccio i vari plot della convergenza e dell'epoch
# Plot reward convergence
plt.title("Cumulative reward per episode")
plt.xlabel("Episode")
plt.ylabel("Cumulative reward")
plt.plot(cum_rewards)
plt.show()

# Plot epoch convergence
plt.title("# epochs per episode")
plt.xlabel("Episode")
plt.ylabel("# epochs")
plt.plot(total_epochs)
plt.show()


#2)TESTING
"""Test della performance della policy dopo la fase di training"""
num_epochs = 0
total_failed_deliveries = 0
num_episodes = 1
experience_buffer = []
store_gif = True #ponilo =False se non lo voglio salvare

for episode in range(1, num_episodes+1):
    # Initialize experience buffer
    my_env = env.reset()
    state = my_env[0]
    epoch = 1
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
        cum_reward += reward

        if reward == -10:
            num_failed_deliveries += 1

        # Store rendered frame in animation dictionary
        experience_buffer.append({
            'frame': env.render(),
            'episode': episode,
            'epoch': epoch,
            'state': state,
            'action': action,
            'reward': cum_reward
            }
        )

        epoch += 1

    total_failed_deliveries += num_failed_deliveries
    num_epochs += epoch

    if store_gif:
        store_episode_as_gif_and_video(experience_buffer)



#Avvio dell'animazione
run_animation(experience_buffer)

# Print dei risultati finali
print("\n")
print(f"Test results after {num_episodes} episodes:")
print(f"Mean # epochs per episode: {num_epochs / num_episodes}")
print(f"Mean # failed drop-offs per episode: {total_failed_deliveries / num_episodes}")

#Fine FASE TESTING