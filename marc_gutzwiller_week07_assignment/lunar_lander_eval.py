from lunar_lander_training import model, model_name
import gymnasium as gym
import imageio

model.load(model_name, device='cpu')

env = gym.make('LunarLander-v3', render_mode='rgb_array')

frames = []
obs, info = env.reset()

for _ in range(1000):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    frames.append(env.render())
    if terminated or truncated:
        break

env.close()

viedeo_path = 'lundar_lander_500k.mp4'
imageio.mimsave(viedeo_path, frames, fps=30)