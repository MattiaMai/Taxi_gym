from configparser import ConfigParser
from board import Board
from metaclasses import Singleton


class Configuration(Board, metaclass=Singleton):
    def __init__(self, inifile):
        super().__init__()
        self.reader = ConfigParser.ConfigParser()
        self.reader.read(inifile)
        self.populate()

    def list_generation(self, section, f, size):
        td = self.section_generation(section)
        retval = map(lambda i: f(td, i), range(0, size))
        return retval

    def section_generation(self, s):
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

    def listFormatting(self, s):
        if (s == '-'):
            retval = None
        else:
            retval = s[1:-1]
            retval = retval.split(',')
        return retval


class RoobokartLearnerConfiguration(Configuration):
    def populate(self):
        # todo: here the code of the configuration of the robokart
        pass
