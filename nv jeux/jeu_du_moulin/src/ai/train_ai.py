from game_env import JeuDuMoulinEnv
from stable_baselines3 import PPO

def train_model():
    env = JeuDuMoulinEnv()  # Initialize the environment
    print("Environment initialized.")
    model = PPO("MlpPolicy", env, verbose=1)  # Create the PPO model
    print("Model created.")
    model.learn(total_timesteps=10000)  # Train the model
    print("Model training completed.")
    model.save("jeu_du_moulin_ai")  # Save the model
    print("Model saved as 'jeu_du_moulin_ai'.")

if __name__ == "__main__":
    train_model()