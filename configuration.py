from configparser import ConfigParser
from board import Board
from metaclasses import Singleton


class Configuration(Board, metaclass=Singleton):
    def __init__(self, inifile):
        super().__init__()
        self.reader = ConfigParser()
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


class RoobokartLearnerConfiguration(Configuration):
    def populate(self):
        sections = ['general', 'graphics', 'report', 'brain', 'hyperparameters', 'environment']
        for section in sections:
            temporary_dictionary = self.section_extraction(section)
            self.merge(temporary_dictionary)
        conversion_list = [
            ('fps', int), ('dpi', int), ('interval', int), ('frame_duration', int),
            ('store_gif', bool), ('epochs', int), ('num_training_episodes', int),
            ('alpha', float), ('gamma', float), ('epsilon', float),
            ('num_test_episodes', int), ('num_rows', int), ('num_columns', int),
            ('window_size_x', int), ('window_size_y', int)
        ]
        for key, to_type in conversion_list:
            self.board[key] = to_type(self.board[key])
        self.board['maps'] = self.board['maps'].split(',')
