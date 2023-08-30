from log import Loggable
from board import Blackboard
import pickle
import glob
import time


# todo: (future work) manage the reaching of the maximum possible number of brains


def last_detected_brain_name():
    conf = Blackboard().get('configuration')
    pattern = conf.get('brain_folder') + conf.get('brain_name') + '_*.' + conf.get('brain_name_suffix')
    files = sorted(glob.glob(pattern), reverse=True)
    retval = None
    if len(files) > 0:
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

#todo: optimize for removing code duplication & video, too
def new_gif_name():
    configuration = Blackboard().get('configuration')
    brain_number = get_last_brain_code() + 1
    digits = configuration.get('brain_name_digits')
    hex_brain_number = hex(brain_number)[2:]
    hex_brain_number = hex_brain_number.rjust(digits, '0')
    file_name = configuration.get('name_gif') + '_' + hex_brain_number + '.gif'
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

def brain_load(filename):
    logger = Loggable('name')
    directory = Blackboard().get('configuration').get('brain_folder')
    fw = open(directory + filename, 'rb')
    q_table = pickle.load(fw)
    fw.close()
    logger.info(f"brain loaded from {filename}")
    return q_table

def report_append(mode, a, g, e, brain_name, mean_reward, mean_failed, mean_epochs):
    now = time.ctime()
    line = now + ';' + mode + ';' + brain_name + ';' + str(a) + ';' + str(g) + ';' + str(e) + ';' + str(mean_reward) + ';' + str(mean_failed) + ';' + str(mean_epochs) + ';\n'
    directory = Blackboard().get('configuration').get('output_folder')
    filename = Blackboard().get('configuration').get('report_file')
    fw = open(directory + filename, 'at')
    fw.write(line)
    fw.close()


def log_episode(episode_number):
    logger = Loggable('main')
    if episode_number % 100 == 0:
        logger.info(f"Episode #: {episode_number}")


def new_video_name():
    configuration = Blackboard().get('configuration')
    brain_number = get_last_brain_code() + 1
    digits = configuration.get('brain_name_digits')
    hex_brain_number = hex(brain_number)[2:]
    hex_brain_number = hex_brain_number.rjust(digits, '0')
    file_name = configuration.get('name_video') + '_' + hex_brain_number + '.mp4'
    return file_name
