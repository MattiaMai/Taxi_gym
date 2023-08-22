from board import Blackboard
from log import Loggable
import numpy as np
from utils import brain_dump
from graphics import reward_plot
import random


def log_episode(episode_number):
    logger = Loggable('main')
    if episode_number % 100 == 0:
        logger.info(f"Episode #: {episode_number}")


def train():
    logger = Loggable('main')
    env = Blackboard().get('environment')
    configuration = Blackboard().get('configuration')
    logger.info("State space: {}".format(env.observation_space))
    logger.info("Action space: {}".format(env.action_space))
    # Initializing the q_table: https://www.gymlibrary.dev/environments/toy_text/taxi/ for details
    q_table = np.zeros([env.observation_space.n, env.action_space.n])
    num_training_episodes = configuration.get('num_training_episodes')
    alpha = configuration.get('alpha')
    gamma = configuration.get('gamma')
    epsilon = configuration.get('epsilon')
    num_epochs = configuration.get('epochs')
    cum_rewards = np.zeros([num_training_episodes])
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
        cum_rewards[episode] = cum_reward
        log_episode(episode)
    brain_file_name = brain_dump(q_table)
    reward_plot(cum_rewards)
    #todo: got to log in the out csv file the quantitative information (also missed delivery)