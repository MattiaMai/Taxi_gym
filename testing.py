from board import Blackboard
from log import Loggable
import numpy as np
from utils import brain_load, log_episode
from graphics import render_episode
import random
from utils import report_append


def test():
    logger = Loggable('main')
    env = Blackboard().get('environment')
    configuration = Blackboard().get('configuration')
    logger.info("State space: {}".format(env.observation_space))
    logger.info("Action space: {}".format(env.action_space))
    # Initializing the q_table: https://www.gymlibrary.dev/environments/toy_text/taxi/ for details
    num_testing_episodes = configuration.get('num_testing_episodes')
    failed_drop_offs = np.zeros([num_testing_episodes])
    cum_rewards = np.zeros([num_testing_episodes])
    brain_file_name = configuration.get('brain_name') + '.' + configuration.get('brain_name_suffix')
    q_table = brain_load(brain_file_name)
    for episode in range(0, num_testing_episodes):
        # Reset environment
        state, info = env.reset()
        execution_steps = []
        num_failed_deliveries = 0
        cum_reward = 0
        done = False
        attempts = 0
        max_attempts = 1000
        while not done and attempts < max_attempts:
            action = np.argmax(q_table[state])
            state, reward, done, _, _ = env.step(action)
            cum_reward += reward
            if reward == -10:
                num_failed_deliveries += 1
            # Store rendered frame in animation dictionary
            execution_steps.append({
                'frame': env.render(),
                'episode': episode,
                'state': state,
                'action': action,
                'reward': cum_reward
            })
            attempts += 1
        render_episode(execution_steps)
        failed_drop_offs[episode] = num_failed_deliveries
        cum_rewards[episode] = cum_reward
        report_append('test', brain_file_name, np.average(cum_rewards), np.average(failed_drop_offs))
