from stable_baselines3 import PPO
from backend.ml4mc_env import ML4MCEnv
from backend.model import Model

  
class RLModel(Model):
    def __init__(self, ml4mc_env: ML4MCEnv, name: str):
        super().__init__(ml4mc_env, name)
        # Load the model (we assume it's a PPO model for now, but this can be changed)
        self.model = PPO.load(self.get_file_path())

    def get_next_action(self, obs):
        return self.model.predict(obs['pov'].copy())[0]

class FightEnemiesModel(RLModel):
    def __init__(self, ml4mc_env: ML4MCEnv):
        super().__init__(ml4mc_env, "fight_enemies_model.pth")