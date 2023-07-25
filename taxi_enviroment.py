from contextlib import closing
from io import StringIO
from os import path
from typing import Optional

import random

import numpy as np

from gym import Env, logger, spaces, utils
from gym.envs.toy_text.utils import categorical_sample
from gym.error import DependencyNotInstalled


num_rows = 10
num_columns = 14

#SI DEVE FAR IN MODO CHE LA SCELTA DELLA MAPPA SIA CONFORME AL NUMERO DI RIGHE O COLONNE INSERITE
'''
10x14
MAP = [
    "+---------------------------+",
    "| : : : : : : : : : : : : : |",
    "| : : : : : : : : : : : : : |",
    "| : |-|-|-|-|-|-| : | | | : |",
    "| : |+:+:+:+:-| : : | | | : |",
    "| : |+:+:+:-| : : | | | | : |",
    "| : |+:+:-| : : | | | | | : |",
    "| : |+:+| : : | | | | | | : |",
    "| : |-|-| : | | | | | | | : |",
    "| : : : : : : : : : : : : : |",
    "| : : : : : : : : : : : : : |",
    "+---------------------------+",
]

10x14
MAP = [
    "+---------------------------+",
    "|-- : : : : : : : : : : : : |",
    "| : | : : : : : : : : : : : |",
    "| : | : : : : : : : : : : : |",
    "| : : : : : : : : : : : : : |",
    "| : : : : : : : : : : : : : |",
    "| : : : : : : : : : : : : : |",
    "| : : : : : : : : : : : : : |",
    "| : : : : : : : : : : : : : |",
    "| : : : : : : : : : : : : : |",
    "| : : : : : : : : : : : : : |",
    "+---------------------------+",
]

10x14
MAP = [
    "+---------------------------+",
    "|-- : : : : : : : : : : : --|",
    "| : : : : : : : : : : : : : |",
    "| : ------------- : ----- : |",
    "| : ----------- : : ----- : |",
    "| : --------- : : ------- : |",
    "| : ------- : : --------- : |",
    "| : ----- : : ----------- : |",
    "| : ----- : ------------- : |",
    "| : : : : : : : : : : : : : |",
    "|-- : : : : : : : : : : : --|",
    "+---------------------------+",
]

5x5
MAP = [
    "+---------+",
    "| : : | : |",
    "| : |-| : |",
    "| | | : | |",
    "| | | |-| |",
    "| | : | : |",
    "+---------+",
]
5x5 che non va
MAP = [
    "+---------+",
    "| : ||| : |",
    "| : ||| : |",
    "| | | : | |",
    "| | | ||| |",
    "| | : ||| |",
    "+---------+",
]

7x7
MAP = [
    "+-------------+",
    "| : : : : : : |",
    "| | : | : ----|",
    "| | : | : : : |",
    "| : : | : : : |",
    "|------ : : : |",
    "| : : : : | | |",
    "| : : : : | | |",
    "+-------------+",
]
'''
MAP = [
    "+---------------------------+",
    "|-- : : : : : : : : : : : --|",
    "| : : : : : : : : : : : : : |",
    "| : ------------- : ----- : |",
    "| : ----------- : : ----- : |",
    "| : --------- : : ------- : |",
    "| : ------- : : --------- : |",
    "| : ----- : : ----------- : |",
    "| : ----- : ------------- : |",
    "| : : : : : : : : : : : : : |",
    "|-- : : : : : : : : : : : --|",
    "+---------------------------+",
]
#si deve scegliere la dimensione in modo conforme alle righe e colonne inserite
#WINDOW_SIZE = (550, 350) #voglio un algoritmo che mi seleziona la risuoluzione adatta
#WINDOW_SIZE = (750, 550) #FANNO USCIRE UNA 7x7 senza linee
#WINDOW_SIZE = (900, 750) #10x14 quasi normale
#WINDOW_SIZE = (900, 700) #QUASI
#WINDOW_SIZE = (900, 650) #SOLO UNA
WINDOW_SIZE = (900, 600) #funzione 10x14
#LA FORMULA SEGRETA E (circa) (x,(x*2)//3)



class TaxiEnv(Env):
    metadata = {
        "render_modes": ["human", "ansi", "rgb_array"],
        "render_fps": 4,
    }

    def __init__(self, render_mode: Optional[str] = None):
        self.desc = np.asarray(MAP, dtype="c")
        print(self.desc)
        print(self.desc[0,0])
        #CREAZIONE DI POSIZIONI CASUALE PER LE CASELLE COLORATE
        coppie = list()
        while len(coppie) < 4:
            x = random.randint(0, num_rows-1) #num_rows-1
            y = random.randint(0, num_columns-1) #num_columns-1
            coppia = (x, y)
            if coppia not in coppie: #spezzo l'if per rendere tutto piu chiaro
                #if self.desc[x + 1, (2 * y) + 1] != b"-" MODIFICA NEL CASO IN CUI ESCLUDO ANCHE |
                if self.desc[x+1,(2*y)+1]==b" ": #E piu facile da vedere che da spiegare, fai la print di self.desc
                    coppie.append(coppia)

        print(coppie)

        #self.locs = locs = [(0, 0), (0, 4), (4, 0), (4, 3)]
        self.locs = locs = coppie
        self.locs_colors = [(255, 0, 0), (0, 255, 0), (255, 255, 0), (0, 0, 255)]

        num_states = num_rows*num_columns*5*4 #5=possibili posizioni passeggero, 4=possibili posizioni albergo

        #num_rows = 6
        #num_columns = 6
        max_row = num_rows - 1
        max_col = num_columns - 1
        self.initial_state_distrib = np.zeros(num_states)
        num_actions = 6
        self.P = {
            state: {action: [] for action in range(num_actions)}
            for state in range(num_states)
        }
        for row in range(num_rows):
            for col in range(num_columns):
                for pass_idx in range(len(locs) + 1):  # +1 for being inside taxi
                    for dest_idx in range(len(locs)):
                        state = self.encode(row, col, pass_idx, dest_idx)
                        if pass_idx < 4 and pass_idx != dest_idx:
                            self.initial_state_distrib[state] += 1
                        for action in range(num_actions):
                            # defaults
                            new_row, new_col, new_pass_idx = row, col, pass_idx
                            reward = (
                                -1
                            )  # default reward when there is no pickup/dropoff
                            terminated = False
                            taxi_loc = (row, col)

                            if action == 0 and self.desc[1 + row +1,2 * col +1]==b" ":
                                new_row = min(row + 1, max_row)
                            elif action == 1 and self.desc[1 + row -1,2 * col +1]==b" ":
                                new_row = max(row - 1, 0)
                            if action == 2 and self.desc[1 + row, 2 * col + 2] == b":":
                                new_col = min(col + 1, max_col)
                            elif action == 3 and self.desc[1 + row, 2 * col] == b":":
                                new_col = max(col - 1, 0)
                            elif action == 4:  # pickup
                                if pass_idx < 4 and taxi_loc == locs[pass_idx]:
                                    new_pass_idx = 4
                                else:  # passenger not at location
                                    reward = -10
                            elif action == 5:  # dropoff
                                if (taxi_loc == locs[dest_idx]) and pass_idx == 4:
                                    new_pass_idx = dest_idx
                                    terminated = True
                                    reward = 20
                                elif (taxi_loc in locs) and pass_idx == 4:
                                    new_pass_idx = locs.index(taxi_loc)
                                else:  # dropoff at wrong location
                                    reward = -10
                            new_state = self.encode(
                                new_row, new_col, new_pass_idx, dest_idx
                            )
                            self.P[state][action].append(
                                (1.0, new_state, reward, terminated)
                            )
        self.initial_state_distrib /= self.initial_state_distrib.sum()
        self.action_space = spaces.Discrete(num_actions)
        self.observation_space = spaces.Discrete(num_states)

        self.render_mode = render_mode

        # pygame utils
        self.window = None
        self.clock = None
        self.cell_size = (
            WINDOW_SIZE[0] / self.desc.shape[1],
            WINDOW_SIZE[1] / self.desc.shape[0],
        )
        self.taxi_imgs = None
        self.taxi_orientation = 0
        self.passenger_img = None
        self.destination_img = None
        self.median_horiz = None
        self.median_vert = None
        self.background_img = None

    def encode(self, taxi_row, taxi_col, pass_loc, dest_idx):
        # (num_rows) num_columns, 5=possibili locazioni passeggero, 4 possibili destinazioni
        i = taxi_row
        i *= num_columns #numero COLONNE
        i += taxi_col
        i *= 5 #numero LOCAZIONI PASSEGGERI
        i += pass_loc
        i *= 4 #numero destinazioni
        i += dest_idx
        return i

    def decode(self, i):
        out = []
        out.append(i % 4)
        i = i // 4 #numero destinazioni
        out.append(i % 5)
        i = i // 5 #numero LOCAZIONI PASSEGGERI
        out.append(i % num_columns)
        i = i // num_columns #numero COLONNE
        out.append(i)
        assert 0 <= i < num_rows #NUMERO RIGHE
        return reversed(out)

    def action_mask(self, state: int):
        """Computes an action mask for the action space using the state information."""
        mask = np.zeros(6, dtype=np.int8)
        taxi_row, taxi_col, pass_loc, dest_idx = self.decode(state)
        if taxi_row < num_rows-1:
            mask[0] = 1
        if taxi_row > 0:
            mask[1] = 1
        if taxi_col < num_columns-1 and self.desc[taxi_row + 1, 2 * taxi_col + 2] == b":":
            mask[2] = 1
        if taxi_col > 0 and self.desc[taxi_row + 1, 2 * taxi_col] == b":":
            mask[3] = 1
        if pass_loc < 4 and (taxi_row, taxi_col) == self.locs[pass_loc]:
            mask[4] = 1
        if pass_loc == 4 and (
            (taxi_row, taxi_col) == self.locs[dest_idx]
            or (taxi_row, taxi_col) in self.locs
        ):
            mask[5] = 1
        return mask

    def step(self, a):
        transitions = self.P[self.s][a]
        i = categorical_sample([t[0] for t in transitions], self.np_random)
        p, s, r, t = transitions[i]
        self.s = s
        self.lastaction = a

        if self.render_mode == "human":
            self.render()
        return (int(s), r, t, False, {"prob": p, "action_mask": self.action_mask(s)})

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[dict] = None,
    ):
        super().reset(seed=seed)
        self.s = categorical_sample(self.initial_state_distrib, self.np_random)
        self.lastaction = None
        self.taxi_orientation = 0

        if self.render_mode == "human":
            self.render()
        return int(self.s), {"prob": 1.0, "action_mask": self.action_mask(self.s)}

    def render(self):
        if self.render_mode is None:
            logger.warn(
                "You are calling render method without specifying any render mode. "
                "You can specify the render_mode at initialization, "
                f'e.g. gym("{self.spec.id}", render_mode="rgb_array")'
            )
        if self.render_mode == "ansi":
            return self._render_text()
        else:  # self.render_mode in {"human", "rgb_array"}:
            return self._render_gui(self.render_mode)

    def _render_gui(self, mode):
        try:
            import pygame  # dependency to pygame only if rendering with human
        except ImportError:
            raise DependencyNotInstalled(
                "pygame is not installed, run `pip install gym[toy_text]`"
            )

        if self.window is None:
            pygame.init()
            pygame.display.set_caption("Taxi")
            if mode == "human":
                self.window = pygame.display.set_mode(WINDOW_SIZE)
            elif mode == "rgb_array":
                self.window = pygame.Surface(WINDOW_SIZE)

        assert (
            self.window is not None
        ), "Something went wrong with pygame. This should never happen."
        if self.clock is None:
            self.clock = pygame.time.Clock()
        if self.taxi_imgs is None:
            file_names = [
                path.join(path.dirname(__file__), "img/cab_front.png"),
                path.join(path.dirname(__file__), "img/cab_rear.png"),
                path.join(path.dirname(__file__), "img/cab_right.png"),
                path.join(path.dirname(__file__), "img/cab_left.png"),
            ]
            self.taxi_imgs = [
                pygame.transform.scale(pygame.image.load(file_name), self.cell_size)
                for file_name in file_names
            ]
        if self.passenger_img is None:
            file_name = path.join(path.dirname(__file__), "img/passenger.png")
            self.passenger_img = pygame.transform.scale(
                pygame.image.load(file_name), self.cell_size
            )

        if self.destination_img is None:
            file_name = path.join(path.dirname(__file__), "img/hotel.png")
            self.destination_img = pygame.transform.scale(
                pygame.image.load(file_name), self.cell_size
            )
            self.destination_img.set_alpha(170)
        if self.median_horiz is None:
            file_names = [
                path.join(path.dirname(__file__), "img/gridworld_median_left.png"),
                path.join(path.dirname(__file__), "img/gridworld_median_horiz.png"),
                path.join(path.dirname(__file__), "img/gridworld_median_right.png"),
            ]
            self.median_horiz = [
                pygame.transform.scale(pygame.image.load(file_name), self.cell_size)
                for file_name in file_names
            ]
        if self.median_vert is None:
            file_names = [
                path.join(path.dirname(__file__), "img/gridworld_median_top.png"),
                path.join(path.dirname(__file__), "img/gridworld_median_vert.png"),
                path.join(path.dirname(__file__), "img/gridworld_median_bottom.png"),
            ]
            self.median_vert = [
                pygame.transform.scale(pygame.image.load(file_name), self.cell_size)
                for file_name in file_names
            ]
        if self.background_img is None:
            file_name = path.join(path.dirname(__file__), "img/taxi_background.png")
            self.background_img = pygame.transform.scale(
                pygame.image.load(file_name), self.cell_size
            )

        desc = self.desc

        for y in range(0, desc.shape[0]):
            for x in range(0, desc.shape[1]):
                cell = (x * self.cell_size[0], y * self.cell_size[1])
                self.window.blit(self.background_img, cell)
                if desc[y][x] == b"|" and (y == 0 or desc[y - 1][x] != b"|"):
                    self.window.blit(self.median_vert[0], cell)
                elif desc[y][x] == b"|" and (
                    y == desc.shape[0] - 1 or desc[y + 1][x] != b"|"
                ):
                    self.window.blit(self.median_vert[2], cell)
                elif desc[y][x] == b"|":
                    self.window.blit(self.median_vert[1], cell)
                elif desc[y][x] == b"-" and (x == 0 or desc[y][x - 1] != b"-"):
                    self.window.blit(self.median_horiz[0], cell)
                elif desc[y][x] == b"-" and (
                    x == desc.shape[1] - 1 or desc[y][x + 1] != b"-"
                ):
                    self.window.blit(self.median_horiz[2], cell)
                elif desc[y][x] == b"-":
                    self.window.blit(self.median_horiz[1], cell)

        for cell, color in zip(self.locs, self.locs_colors):
            color_cell = pygame.Surface(self.cell_size)
            color_cell.set_alpha(128)
            color_cell.fill(color)
            loc = self.get_surf_loc(cell)
            self.window.blit(color_cell, (loc[0], loc[1] + 10))

        taxi_row, taxi_col, pass_idx, dest_idx = self.decode(self.s)

        if pass_idx < 4:
            self.window.blit(self.passenger_img, self.get_surf_loc(self.locs[pass_idx]))

        if self.lastaction in [0, 1, 2, 3]:
            self.taxi_orientation = self.lastaction
        dest_loc = self.get_surf_loc(self.locs[dest_idx])
        taxi_location = self.get_surf_loc((taxi_row, taxi_col))

        if dest_loc[1] <= taxi_location[1]:
            self.window.blit(
                self.destination_img,
                (dest_loc[0], dest_loc[1] - self.cell_size[1] // 2),
            )
            self.window.blit(self.taxi_imgs[self.taxi_orientation], taxi_location)
        else:  # change blit order for overlapping appearance
            self.window.blit(self.taxi_imgs[self.taxi_orientation], taxi_location)
            self.window.blit(
                self.destination_img,
                (dest_loc[0], dest_loc[1] - self.cell_size[1] // 2),
            )

        if mode == "human":
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])
        elif mode == "rgb_array":
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(self.window)), axes=(1, 0, 2)
            )

    def get_surf_loc(self, map_loc):
        return (map_loc[1] * 2 + 1) * self.cell_size[0], (
            map_loc[0] + 1
        ) * self.cell_size[1]

    def _render_text(self): #RENDERTEX NON LO USIAMO, QUINDI NON LO TOCCO
        desc = self.desc.copy().tolist()
        outfile = StringIO()

        out = [[c.decode("utf-8") for c in line] for line in desc]
        taxi_row, taxi_col, pass_idx, dest_idx = self.decode(self.s)

        def ul(x):
            return "_" if x == " " else x

        if pass_idx < 4:
            out[1 + taxi_row][2 * taxi_col + 1] = utils.colorize(
                out[1 + taxi_row][2 * taxi_col + 1], "yellow", highlight=True
            )
            pi, pj = self.locs[pass_idx]
            out[1 + pi][2 * pj + 1] = utils.colorize(
                out[1 + pi][2 * pj + 1], "blue", bold=True
            )
        else:  # passenger in taxi
            out[1 + taxi_row][2 * taxi_col + 1] = utils.colorize(
                ul(out[1 + taxi_row][2 * taxi_col + 1]), "green", highlight=True
            )

        di, dj = self.locs[dest_idx]
        out[1 + di][2 * dj + 1] = utils.colorize(out[1 + di][2 * dj + 1], "magenta")
        outfile.write("\n".join(["".join(row) for row in out]) + "\n")
        if self.lastaction is not None:
            outfile.write(
                f"  ({['South', 'North', 'East', 'West', 'Pickup', 'Dropoff'][self.lastaction]})\n"
            )
        else:
            outfile.write("\n")

        with closing(outfile):
            return outfile.getvalue()

    def close(self):
        if self.window is not None:
            import pygame

            pygame.display.quit()
            pygame.quit()


# Taxi rider from https://franuka.itch.io/rpg-asset-pack
# All other assets by Mel Tillery http://www.cyaneus.com/
