from typing import Tuple
import numpy.random as random

class point():

    def __init__(self, x=0, y=0) -> None:

        self.xpos = x
        self.ypos = y


    def randomize(self, lim) -> None:

        self.xpos = random.randint(low=1, high=lim)
        self.ypos = random.randint(low=1, high=lim)


    def __getitem__ (self, key) -> int:

        return (self.xpos, self.ypos)[key]

    def __call__(self) -> Tuple:

        return (self.xpos, self.ypos)

    def __eq__(self, other) -> bool:

        return True if ((self.xpos == other.xpos) and (self.ypos == other.ypos)) else False

    def move(self, direction: str) -> None:

        if direction == "up":
            self.xpos -= 1
        elif direction == "down":
            self.xpos += 1
        elif direction == "left":
            self.ypos -= 1
        elif direction == "right":
            self.ypos += 1

    def update_pos(self, x: int, y: int):

        self.xpos = x
        self.ypos = y
