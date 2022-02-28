from gym.envs.registration import register

# registra o env como pacote para ser usado com gym.make()
register(
    id='SnakeRuim-v0',
    entry_point='snake_ruim.envs:snake_env',
)
