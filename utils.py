from log import Loggable
from board import Blackboard
from datetime import datetime
import pickle
import glob
from math import pow


#todo: manage the reaching of the maximum possible brain number

def last_detected_brain_name():
    conf = Blackboard().get('configuration')
    pattern = conf.get('brain_folder') + conf.get('brain_name') + '_*.' + conf.get('brain_name_suffix')
    files = sorted(glob.glob(pattern), reverse=True)
    retval = None
    if len(files) > 0:
        # todo: debugging the case where a file already exists
        file_name = files[0]
        prefix = conf.get('brain_folder') + conf.get('brain_name') + '_'
        starting_point = len(prefix)
        ending_point = starting_point + conf.get('brain_name_digits')
        retval = file_name[starting_point:ending_point]
    return retval


def get_last_brain_code():
    brain_name = last_detected_brain_name()
    retval = -1
    if brain_name is not None:
        retval = int(brain_name, 16)
    return retval


def new_brain_name():
    configuration = Blackboard().get('configuration')
    brain_number = get_last_brain_code() + 1
    digits = configuration.get('brain_name_digits')
    hex_brain_number = hex(brain_number)[2:]
    hex_brain_number = hex_brain_number.rjust(digits, '0')
    file_name = configuration.get('brain_name') + '_' + hex_brain_number + '.' + configuration.get('brain_name_suffix')
    return file_name


def brain_dump(qtable):
    logger = Loggable('name')
    directory = Blackboard().get('configuration').get('brain_folder')
    filename = new_brain_name()
    fw = open(directory + filename, 'wb')
    pickle.dump(qtable, fw)
    fw.close()
    logger.info(f"brain saved as {filename}")
    return filename

# def report_append(mode,brain_name,reward,)
