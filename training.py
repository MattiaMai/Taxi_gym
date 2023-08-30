from board import Blackboard
from log import Loggable
import numpy as np

from map import mutate
from utils import brain_dump, log_episode
from graphics import reward_plot, dropoffs_plot
import random
from utils import report_append

def train():
    logger = Loggable('main')
    env = Blackboard().get('environment')
    configuration = Blackboard().get('configuration')
    logger.info("State space: {}".format(env.observation_space))
    logger.info("Action space: {}".format(env.action_space))
    # Initializing the q_table: https://www.gymlibrary.dev/environments/toy_text/taxi/ for details
    q_table = np.zeros([env.observation_space.n, env.action_space.n])
    alpha = configuration.get('alpha') * (1 + random.uniform(-0.5,0.5))
    gamma = configuration.get('gamma') * (1 + random.uniform(-0.5,0.5))
    epsilon = configuration.get('epsilon') * (1 + random.uniform(-0.5,0.5))
    failed_drop_offs = list()
    cum_rewards = list()
    epochs = list()
    num_training_episodes = configuration.get('num_training_episodes')
    num_epochs = configuration.get('epochs')
    num_experiments = configuration.get('num_training_experiments')
    for experiment in range(0,num_experiments):
        map = mutate()
        Blackboard().put('locs',map)
        for episode in range(0, num_training_episodes):
            # Reset environment
            state, info = env.reset()
            num_failed_drop_offs = 0
            done = False
            cum_reward = 0
            epoch = 0
            while not done and epoch < num_epochs:
                if random.uniform(0, 1) < epsilon:
                    action = env.action_space.sample()  # Sample random action (exploration)
                else:
                    action = np.argmax(q_table[state])  # Select best known action (exploitation)
                next_state, reward, done, _, info = env.step(action)
                cum_reward += reward
                old_q_value = q_table[state, action]
                next_max = np.max(q_table[next_state])
                new_q_value = (1 - alpha) * old_q_value + alpha * (reward + gamma * next_max)
                q_table[state, action] = new_q_value
                if reward == -10:
                    num_failed_drop_offs += 1
                state = next_state
                epoch += 1
        epochs.append(epoch)
        failed_drop_offs.append(num_failed_drop_offs)
        cum_rewards.append(cum_reward)
        log_episode(episode)
    brain_file_name = brain_dump(q_table)
    #reward_plot(cum_rewards)
    #dropoffs_plot(failed_drop_offs)
    avg = lambda x: sum(x)/len(x)
    report_append('train', alpha, gamma, epsilon, brain_file_name, avg(cum_rewards), avg(failed_drop_offs), avg(epochs))

