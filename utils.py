from log import Loggable
from board import Blackboard
import pickle


def brain_dump(qtable):
    logger = Loggable('name')
    filename = Blackboard().get('configuration').get('brain_name')
    fw = open(filename, 'wb')
    pickle.dump(qtable, fw)
    fw.close()
    logger.info(f"brain saved as {filename}")