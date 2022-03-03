from typing import Tuple
from os import system
from time import sleep
from colorama import init
import gym
from gym import spaces
import numpy as np
from termcolor import colored

from snake_ruim.utils.support_funcs import point


class snake_env(gym.Env):

    def __init__(self, size=10) -> None:

        super(snake_env, self).__init__()


        self.field_size : int = size
        #criando espaco de observacoes
        self.observation_space = spaces.Dict({
                                            "snake_positionx" : spaces.Discrete(self.field_size), 
                                            "snake_positiony" : spaces.Discrete(self.field_size),
                                            "candy_positionx" : spaces.Discrete(self.field_size), 
                                            "candy_positiony" : spaces.Discrete(self.field_size),
                                            "poison_positionx": spaces.Discrete(self.field_size), 
                                            "poison_positiony" : spaces.Discrete(self.field_size),
                                            #estados das quatro celulas vizinhas (podem ser [vazio, parede, veneno, doce])
                                            "up"    : spaces.Discrete(5),
                                            "down"  : spaces.Discrete(5),
                                            "left"  : spaces.Discrete(5),
                                            "right" : spaces.Discrete(5)
                                             })

        self.step_count = 0
        #espaco de acoes discreto (cima, baixo, direita, esquerda)
        self.action_space = spaces.Discrete(4)

        #inicializando posicoes
        self.doce_pos = point()
        self.veneno_pos = point()
        self.snake_pos = point()

        #inicializando campo
        self.field = np.zeros((self.field_size, self.field_size), dtype=np.int32)
        self._write_field()

    def _write_field(self) -> None:
        """
        0: vazio
        1: parede
        2: veneno
        3: doce
        4: cobra
        """
        with np.nditer(self.field, flags=["multi_index"]) as it:

            for _ in it:
                # montando paredes
                if (it.multi_index[0] == 0) or (it.multi_index[1] == 0) or (it.multi_index[0] == (self.field_size - 1)) or (it.multi_index[1] == (self.field_size - 1)):

                    self.field[it.multi_index] = 1

                #posicionando venenos
                elif it.multi_index == self.veneno_pos():

                    self.field[it.multi_index] = 2

                #posicionando doce
                elif it.multi_index == self.doce_pos():

                    self.field[it.multi_index] = 3
 
                #posicionando cobra
                elif it.multi_index == self.snake_pos():

                    self.field[it.multi_index] = 4

                #vazios
                else:
                    self.field[it.multi_index] = 0




    def _generate_doces(self) -> None:
        """
        gera uma posicao aleatoria do doce e do veneno diferentes entre si
        """

        self.doce_pos.randomize(lim=(self.field_size - 1))
        self.veneno_pos.randomize(lim=(self.field_size - 1))

        #garante que posicao do doce e do veneno sao diferentes
        if (self.doce_pos == self.veneno_pos):
            self._generate_doces()


    def reset(self):

        #posicao do personagem
        self.snake_pos.update_pos(int(self.field_size/2), int(self.field_size/2))


        #inicializa posicao dos doces
        self._generate_doces()

        self.episode_return = 0
        self.step_count = 0

        obs = {
            "snake_positionx" : self.snake_pos[0], 
            "snake_positiony" : self.snake_pos[1],
            "candy_positionx" : self.doce_pos[0], 
            "candy_positiony" : self.doce_pos[1],
            "poison_positionx": self.veneno_pos[0], 
            "poison_positiony": self.veneno_pos[1],
            #estados das quatro celulas vizinhas (podem ser [vazio, parede, veneno, doce])
            "up"    : self.field[self.snake_pos[0] - 1, self.snake_pos[1]].item(),
            "down"  : self.field[self.snake_pos[0] + 1, self.snake_pos[1]].item(),
            "left"  : self.field[self.snake_pos[0], self.snake_pos[1] - 1].item(),
            "right" : self.field[self.snake_pos[0], self.snake_pos[1] + 1].item()
        }

        self._write_field()

        return obs

    def render(self, mode="console"):

        if mode != "console":
            raise NotImplementedError()

        system("clear")
        #necessario para printar cores no terminal
        init()

        print(f"Episode return = {self.episode_return}\nTotal steps = {self.step_count}")

        with np.nditer(self.field, flags=["multi_index"]) as it:

            for cell in it:
                # montando paredes
                if cell == 1:

                    print("#", end="")
                    if it.multi_index[1] == (self.field_size - 1):
                        #adiciona \n no final do campo
                        print("")

                #posicionando venenos
                elif cell == 2:

                    print(colored("0", "red"), end="")

                #posicionando doce
                elif cell == 3:

                    print(colored("0", "green"), end="")
 
                #posicionando cobra
                elif cell == 4:

                    print(colored("C", "blue"), end="")

                #vazios
                else:
                    print(" ", end="")

        sleep(0.5)

    def _take_action(self, action):

        if action == 0:
            self.snake_pos.move("up")
        elif action == 1:
            self.snake_pos.move("down")
        elif action == 2:
            self.snake_pos.move("left")
        elif action == 3:
            self.snake_pos.move("right")

    def _obs(self):

        obs = {
            "snake_positionx" : self.snake_pos[0], 
            "snake_positiony" : self.snake_pos[1],
            "candy_positionx" : self.doce_pos[0], 
            "candy_positiony" : self.doce_pos[1],
            "poison_positionx": self.veneno_pos[0], 
            "poison_positiony": self.veneno_pos[1],
            #estados das quatro celulas vizinhas (podem ser [vazio, parede, veneno, doce])
            "up"    : self.field[self.snake_pos[0] - 1, self.snake_pos[1]].item(),
            "down"  : self.field[self.snake_pos[0] + 1, self.snake_pos[1]].item(),
            "left"  : self.field[self.snake_pos[0], self.snake_pos[1] - 1].item(),
            "right" : self.field[self.snake_pos[0], self.snake_pos[1] + 1].item()
        }

        return obs

    def _calculate_reward(self) -> Tuple[float, bool]:

        reward = 0
        done = False

        if self.snake_pos == self.doce_pos:

            reward += 100
            self._generate_doces()

        elif self.snake_pos == self.veneno_pos:

            reward -= 100
            self._generate_doces()
            done = True

        elif (self.snake_pos[0] == 0) or (self.snake_pos[1] == 0) or (self.snake_pos[0] == (self.field_size - 1)) or (self.snake_pos[1] == (self.field_size - 1)):

            reward -= 100
            done = True


        return reward, done

    def _print_info(self, action):
        print(f"{self.snake_pos()=}")
        print(f"{self.doce_pos()=}")
        print(f"{self.veneno_pos()=}")
        print(f"{action=}")
        self.render()

    def step(self, action):
        """
        acoes validas: {cima:0, baixo:1, esquerda:2, direita:3}
        """

        #move o personagem na direcao de "action"
        self._take_action(action)

        # self._print_info(action)
        #retorna dicionario com as observacoes atuais
        reward, done = self._calculate_reward()

        if not(done):
            obs = self._obs()
        else:
            obs = {}
        self.episode_return += reward
        self.step_count += 1

        self._write_field()

        return obs, reward, done, {}
