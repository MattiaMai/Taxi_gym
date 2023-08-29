import configparser
from board import Board
from metaclasses import Singleton


class Configuration(Board, metaclass=Singleton):
    def __init__(self, inifile):
        super().__init__()
        self.reader = configparser.ConfigParser()
        self.reader.read(inifile)
        self.populate()

    def list_generation(self, section, f, size):
        td = self.section_extraction(section)
        retval = map(lambda i: f(td, i), range(0, size))
        return retval

    def section_extraction(self, s):
        temp = dict()
        options = self.reader.options(s)
        for o in options:
            try:
                temp[o] = self.reader.get(s, o)
                if temp[o] == -1:
                    print("skip: %s" % o)
            except:
                print("exception on %s!" % o)
                temp[o] = None
        return temp

    def populate(self):
        pass

    def list_extraction(self, s):
        if s == '-':
            retval = None
        else:
            retval = s[1:-1]
            retval = retval.split(',')
        return retval

def mybool(tobool):
    return tobool == 'True'

class RoobokartLearnerConfiguration(Configuration):
    def populate(self):
        sections = ['general', 'graphics', 'training', 'testing', 'hyperparameters', 'environment']
        for section in sections:
            temporary_dictionary = self.section_extraction(section)
            self.merge(temporary_dictionary)
        conversion_list = [
            ('brain_name_digits', int), ('fps', int), ('dpi', int), ('interval', int), ('frame_duration', int),
            ('store_gif', mybool), ('epochs', int), ('alpha', float), ('gamma', float),
            ('epsilon', float),
            ('num_testing_episodes', int), ('num_testing_experiments', int),
            ('num_training_episodes', int), ('num_training_experiments', int),
            ('num_rows', int), ('num_columns', int),
            ('window_size_x', int), ('window_size_y', int)
        ]
        for key, to_type in conversion_list:
            self.board[key] = to_type(self.board[key])
