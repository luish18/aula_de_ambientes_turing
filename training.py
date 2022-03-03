from stable_baselines3.ppo.ppo import PPO
from snake_ruim.envs.snake_ruim import snake_env
import gym

def main():

    #creating env
    env = gym.make("SnakeRuim-v0", size=20)


    #creating and training model
    model = PPO("MultiInputPolicy", env, verbose=1).learn(500000)

    # Test the trained agent
    obs = env.reset()
    n_steps = 100
    for step in range(n_steps):

        action, _ = model.predict(obs, deterministic=True)
        print("Step {}".format(step + 1))
        print("Action: ", action)
        obs, reward, done, _ = env.step(action)
        print('obs=', obs, 'reward=', reward, 'done=', done)
        env.render(mode='console')
        if done:
            # Note that the VecEnv resets automatically
            # when a done signal is encountered
            print("Goal reached!", "reward=", reward)
            break

if __name__ == "__main__":
    main()
