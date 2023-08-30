from random import randint
from board import Blackboard

mapkb = {
    "alpha": (
        ["+---------+","| : : | : |","| : |-| : |","| | | : | |","| | | |-| |","| | : | : |","+---------+",],
        (550, 350),
        5,
        5),
    "beta": (
        ["+---------------------------+","| : : : : : : : : : : : : : |","| : : : : : : : : : : : : : |","| : |-|-|-|-|-|-| : | | | : |","| : |+:+:+:+:-| : : | | | : |","| : |+:+:+:-| : : | | | | : |","| : |+:+:-| : : | | | | | : |","| : |+:+| : : | | | | | | : |","| : |-|-| : | | | | | | | : |","| : : : : : : : : : : : : : |","| : : : : : : : : : : : : : |","+---------------------------+",],
        (900, 600),
        10,
        14)
}


def load_map(map_name):
    retval = mapkb[map_name]
    return retval

def mutate():
    b = Blackboard()
    desc = b.get('map')
    nrow = b.get('nrow')
    ncol = b.get('ncol')
    retval = list()
    while len(retval) < 4:
        x = randint(0, nrow - 1)  # num_rows-1
        y = randint(0, ncol - 1)  # num_columns-1
        coppia = (x, y)
        if coppia not in retval:
            if desc[x + 1, (2 * y) + 1] == b" ":
                retval.append(coppia)
    return retval