import sys
from board import Blackboard
from configuration import RoobokartLearnerConfiguration
from experimenting import experiment
from log import LoggerFactory, Loggable
from training import train
from testing import test
import gym

modes = {
    'train': train,
    'test': test,
    'experiment': experiment
}



if __name__ == '__main__':
    if len(sys.argv) >= 3:
        blackboard = Blackboard()
        mode = sys.argv[1]
        configuration_filename = sys.argv[2]
        loops = 1
        configuration = RoobokartLearnerConfiguration(configuration_filename)
        blackboard.put('configuration', configuration)
        if len(sys.argv) >= 4:
            loops = int(sys.argv[3])
        for i in range(0,loops):
            environment = gym.make(configuration.get('env_name'), render_mode=configuration.get('render_mode'))
            blackboard.put('environment', environment)
            LoggerFactory.setup(configuration)
            logger = Loggable('main')
            logger.info('Run starting')
            modes[mode]()
        logger.info('Run ending')
        LoggerFactory.shutdown()
        print('Have a nice day :)')
        exit(0)

