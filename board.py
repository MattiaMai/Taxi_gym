from metaclasses import Singleton


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


class Blackboard(Board, metaclass=Singleton):
    def __init__(self):
        super().__init__()
