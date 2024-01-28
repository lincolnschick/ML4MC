import minerl
import gym
from minerl.herobraine.env_specs.ml4mc_survival_specs import ML4MCSurvival

class ModelSwapper():
    def __init__(self):
        self.loadedEnvironment = ""
        self.progress = 0
        self.paused = False
    
    def load_environment():
        ml4mc_survival = ML4MCSurvival()
        ml4mc_survival.register()
        env = gym.make('ML4MCSurvival-v0')
        env.reset()