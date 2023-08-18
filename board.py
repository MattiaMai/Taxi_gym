class Board:
    def __init__(self):
        self.board = dict()

    def get(self, key):
        return self.board[key]

    def put(self, key, value):
        self.board[key] = value

    def merge(self, dic):
        self.board.update(dic)

    def board_merge(self, dic):
        self.board.update(dic.board)

    def size(self):
        return len(self.board.keys())

#todo: define the blackboard as a way to share environments, etc.

class AbstractBoardFactory():
    def __init__(self):
        self.mapping = {
            'years': self.years,
            'mins': self.mins,
            'days': self.days,
            'hours': self.hours,
            'secs': float,
            'int': int,
            'float': float,
            'm_sec': float,
            'km_h': self.kmh,
            'bool': self.bools,
            'km': self.km
        }

    def km(self, val):
        temp = float(val) * 1000
        return temp

    def years(self, yrs):
        temp = 365 * float(yrs)
        temp = self.days(temp)
        return temp

    def kmh(self, kmh):
        temp = float(kmh) / 3.6
        return temp

    def days(self, dys):
        temp = 24 * float(dys)
        temp = self.hours(temp)
        return temp

    def bools(self, str):
        temp = str == 'True'
        return temp

    def mins(self, dys):
        temp = 60 * float(dys)
        return temp

    def split(self, value):
        index = value.rfind(',')
        return value[0:index], value[index + 1:]

    def hours(self, hrs):
        temp = float(hrs) * 3600
        return temp

    def process(self, value):
        vals = self.split(value)
        f = self.mapping[vals[-1]]
        retval = f(vals[0])
        return retval

    def processable(self, value):
        val, func = self.split(value)
        found = False
        try:
            found = func in self.mapping.keys()
        except TypeError:
            pass
        return found

    def tolist(self, value):
        retval = value.split(',')
        return retval

    def loadSection(self, reader, s):
        temp = dict()
        options = reader.options(s)
        for o in options:
            try:
                value = reader[s][o]
                if self.processable(value):
                    value = self.process(value)
                temp['[' + s + ']' + o] = value
            except:
                print("exception on %s!" % o)
                temp[o] = None
        return temp
