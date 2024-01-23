# Requirement 25 Report
## Overview
This script was created to provide an exit for the AI agent if it gets lost/very deep underground. 
It can be difficult for even human players to find their way out from a cave, so it is important that the AI agent has a way to get out.

## Custom Environment
In order to give the script access to everything it needs (knowledge of the inventory, equipped items, coordinates, camera angles, and sky visibility), I created a new custom environment called ML4MCSurvival. This can be modified as we continue development and can be the environment we use for showcasing our AI agent.

## Features
Developing the script involved accounting for a variety of scenarios.
The script is able to approach a wall if we are not already there,
move the agent to the center of a block so it can fit through a 1 block wide staircase,
and adjust the agent's camera to look at the proper blocks to mine in a staircase pattern.
Additionally, the script works with a bare fist or a wooden, stone, or iron pickaxe by adjusting how long to mine each block.
The script can handle instances of the mining tool breaking during the ascent as well.
Lastly, it can handle semi-unexpected blocks appearing in ascent such as ore or wood (although not very elegantly).
The script may not work if the agent mines into lava/water or is directly below sand/gravel (it is ok if it is in front of it though).

## Links
The source code can be found at [mine_to_surface.py](https://github.com/lincolnschick/ML4MC/blob/1090b1dae0a01a930d2e299e112c06a1a8232703/src/scripts/mine_to_surface.py).

The custom environment can be found at [ml4mc_survival_specs.py](https://github.com/lincolnschick/minerl/blob/856cefa32504867bc4efd062cbf2cc8937966591/minerl/herobraine/env_specs/ml4mc_survival_specs.py).

The video can be found at [mine_to_surface_demo.mp4](https://github.com/lincolnschick/ML4MC/blob/1090b1dae0a01a930d2e299e112c06a1a8232703/docs/reports/requirement-31/mine_to_surface_demo.mp4).
