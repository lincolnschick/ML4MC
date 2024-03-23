from enum import Enum

# Identifying Objective for Agent
class Objective(Enum):
    IRON = 1
    STONE = 2
    WOOD = 3
    ENEMIES = 4

# Identifying Script for Agent
class Script(Enum):
    DIAMOND = 1
    STONE = 2
    PLACEHOLDER = 3
    SURFACE = 4
    PICKAXE = 5
    SWORD = 6

# Messages passed through Queues
class Message(Enum):
    PAUSE_AGENT = 1
    PLAY_AGENT = 2
    RESTART = 3
    RESTART_FINISHED = 4    
    SCRIPT_FINISHED = 5
    START_RECORDING = 6
    STOP_RECORDING = 7
    QUIT = 8

