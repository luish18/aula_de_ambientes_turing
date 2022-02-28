from typing import Tuple
import gym
from gym import spaces
from snake_ruim.utils.support_funcs import point
import numpy as np


class snake_env(gym.Env):

    def __init__(self, size=10) -> None:

        super(snake_env, self).__init__()


        self.field_size : int = size

        #criando espaco de observacoes
        self.observation_space = spaces.Dict({  #                                 posx                              posy
                                                 "snake_position" : spaces.Tuple((spaces.Discrete(self.field_size), spaces.Discrete(self.field_size))),
                                                 "candy_position" : spaces.Tuple((spaces.Discrete(self.field_size), spaces.Discrete(self.field_size))),
                                                 "poison_position": spaces.Tuple((spaces.Discrete(self.field_size), spaces.Discrete(self.field_size))),
                                                #estados das quatro celulas vizinhas (podem ser [vazio, parede, veneno, doce])
                                                 "neighbor_cells" : spaces.Dict({
                                                                                    "up"    : spaces.Discrete(4),
                                                                                    "down"  : spaces.Discrete(4),
                                                                                    "left"  : spaces.Discrete(4),
                                                                                    "right" : spaces.Discrete(4)
                                                                                })
                                             })

        self.step_count = 0
        #espaco de acoes discreto (cima, baixo, direita, esquerda)
        self.action_space = spaces.Discrete(4)

        #inicializando posicoes
        self.doce_pos = point()
        self.veneno_pos = point()
        self.snake_pos = point()

        #inicializando campo
        self.field = np.zeros((self.field_size, self.field_size))
        self._reset_field()

    def _reset_field(self) -> None:

        it = np.nditer(self.field, flags=["multi_index"])

        for _ in it:
            # montando paredes
            if (it.multi_index[0] == 0) or (it.multi_index[1] == 0) or (it.multi_index[0] == (self.field_size - 1)) or (it.multi_index[1] == (self.field_size - 1)):
                self.field[it.multi_index] = 1
            else:
                self.field[it.multi_index] = 1



    def _generate_doces(self) -> None:
        """
        gera uma posicao aleatoria do doce e do veneno diferentes entre si
        """

        self.doce_pos.randomize(lim=self.field_size)
        self.veneno_pos.randomize(lim=self.field_size)

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
            "snake_position" : self.snake_pos(),
            "candy_position" : self.doce_pos(),
            "poison_position": self.veneno_pos(),
            "neighbor_cells" : {
                "up"         : self.field[self.snake_pos[0] - 1, self.snake_pos[1]],
                "down"       : self.field[self.snake_pos[0] + 1, self.snake_pos[1]],
                "left"       : self.field[self.snake_pos[0], self.snake_pos[1] - 1],
                "right"      : self.field[self.snake_pos[0], self.snake_pos[1] + 1]
            }
        }

        return obs

    #TODO: write render method
    def render(self, mode="human"):


        return super().render(mode)


    def _take_action(self, action):

        if action == 0:
            self.snake_pos.move("up")
        elif action == 1:
            self.snake_pos.move("down")
        elif action == 2:
            self.snake_pos.move("left")
        elif action == 3:
            self.snake_pos.move("right")

    def _next_obs(self):

        obs = {
            "snake_position" : self.snake_pos(),
            "candy_position" : self.doce_pos(),
            "poison_position": self.veneno_pos(),
            "neighbor_cells" : {
                "up"         : self.field[self.snake_pos[0] - 1, self.snake_pos[1]],
                "down"       : self.field[self.snake_pos[0] + 1, self.snake_pos[1]],
                "left"       : self.field[self.snake_pos[0], self.snake_pos[1] - 1],
                "right"      : self.field[self.snake_pos[0], self.snake_pos[1] + 1]
            }
        }

        return obs

    def _calculate_reward(self) -> Tuple[float, bool]:

        reward = 0
        done = False

        if self.snake_pos == self.doce_pos:

            reward += 10
            self._generate_doces()

        elif self.snake_pos == self.veneno_pos:

            reward -= 100
            done = True

        elif (self.snake_pos[0] == 0) or (self.snake_pos[1] == 0) or (self.snake_pos[0] == self.field_size) or (self.snake_pos[1] == self.field_size):

            reward -= 100
            done = True

        else:

            reward += 1

        return reward, done


    def step(self, action):
        """
        acoes validas: {cima:0, baixo:1, esquerda:2, direita:3}
        """

        #move o personagem na direcao de "action"
        self._take_action(action)

        #retorna dicionario com as observacoes atuais
        obs = self._next_obs()
        reward, done = self._calculate_reward()


        return obs, reward, done, {}
