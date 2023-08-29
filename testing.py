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
    alpha = configuration.get('alpha')
    gamma = configuration.get('gamma')
    epsilon = configuration.get('epsilon')
    failed_drop_offs = np.zeros([num_testing_episodes])
    cum_rewards = np.zeros([num_testing_episodes])
    q_table = brain_load(configuration.get('brain_name') + '.' + configuration.get('brain_name_suffix'))
    for episode in range(0, num_testing_episodes):
        # Reset environment
        state, info = env.reset()
        execution_steps = []
        num_failed_deliveries = 0
        cum_reward = 0
        done = False
        while not done:
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
        render_episode(execution_steps)
    # Avvio dell'animazione
    # run_animation(experience_buffer) #commenta l'animazione per rendere tutto più server-friendly

    # Print dei risultati finali
    print("\n")
    print(f"Test results after {num_episodes} episodes:")
    print(f"Mean # failed drop-offs per episode: {total_failed_deliveries / num_episodes}")

    # Fine FASE TESTING


total_failed_deliveries += num_failed_deliveries

