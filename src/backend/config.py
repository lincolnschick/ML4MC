"""
Configuration file for ML4MC. This file should define frequently used
constants that are passed across different parts of the codebase.
"""

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
    SURFACE = 3
    PICKAXE = 4
    SWORD = 5
    TORCH = 6
    HOUSE = 7

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

