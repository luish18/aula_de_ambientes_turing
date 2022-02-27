import gym
from gym import spaces
import numpy.random as random

class snake_env(gym.Env):

    def __init__(self, size=10) -> None:

        super(snake_env, self).__init__()


        self.field_size = size

                         #posx da cobra                     posy da cobra
        self.obs_shape = (spaces.Discrete(self.field_size), spaces.Discrete(self.field_size),
                         #posx do veneno                    posy do veneno
                          spaces.Discrete(self.field_size), spaces.Discrete(self.field_size),
                         #posx do doce                      posy do doce
                          spaces.Discrete(self.field_size), spaces.Discrete(self.field_size),
                         #celulas vizinhas up, down, left, right (podem ser vazio, parede, doce ou veneno)
                          spaces.Discrete(4), spaces.Discrete(4), spaces.Discrete(4), spaces.Discrete(4))


        #criando espaco de observacoes
        self.observation_space = spaces.Tuple(self.obs_shape)

        #espaco de acoes discreto (cima, baixo, direita, esquerda)
        self.action_space = spaces.Discrete(4)


    def _generate_doces(self):
        """
        gera uma posicao aleatoria do doce e do veneno diferentes entre si
        """

        while (self.veneno_pos == self.doce_pos):
            self.doce_pos = (random.randint(low=1, high=(self.field_size - 1)), random.randint(low=1, high=(self.field_size - 1)))
            self.veneno_pos = (random.randint(low=1, high=(self.field_size - 1)), random.randint(low=1, high=(self.field_size - 1)))

        return self.doce_pos, self.veneno_pos


    def reset(self):

        #TODO:create point class and separate class for different objects in the game
        #posicao do personagem
        self.snake_pos = (0, 0)


        #inicializa posicao dos doces
        self.doce_pos = (0,0)
        self.veneno_pos = (0,0)

        #gera posicao aleatoria dos doces diferente da posicao do personagem
        while (self.doce_pos == self.snake_pos) or (self.veneno_pos == self.snake_pos):
            self._generate_doces()

        self.episode_reward = 0

    #TODO: finish this function
    def _next_observation(self):
        pass


    def step(self, action):
        """
        acoes validas: {cima:0, baixo:1, esquerda:2, direita:3}
        """

        #checando se a acao e valida
        assert self.action_space.contains(action), "Invalid Action"

        #TODO: turn moving logic into separate function
        #muda a posicao do personagem de acordo com a acao tomada
        current_pos = self.snake_pos
        if action == 0:
            self.snake_pos = (current_pos[0] + 1, current_pos[1])

        elif action == 1:
            self.snake_pos = (current_pos[0] - 1, current_pos[1])

        elif action == 2:
            self.snake_pos = (current_pos[0], current_pos[1] - 1)

        elif action == 3:
            self.snake_pos = (current_pos[0], current_pos[1] + 1)


        #TODO: turn reward logic into separate function
        reward = 0
        #calcula recompensa
        if self.snake_pos == self.doce_pos:
            reward = 1.0
            done = False

        #termina jogo se o personagem comer um veneno
        elif self.snake_pos == self.veneno_pos:
            reward = 10.0
            done = True

        #termina o jogo caso o personagem entre na parede
        elif (self.snake_pos[0] == 0) or (self.snake_pos[0] == self.field_size) or (self.snake_pos[1] == 0) or (self.snake_pos[1] == self.field_size):
            reward = 5.0
            done = True

        else:
            done = False


        self.episode_reward += reward
        obs = self._next_observation

        return obs, reward, done, {}
