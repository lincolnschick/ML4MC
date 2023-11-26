# Requirement 25 Report
The scripting for stone collection was fairly straightforward.
I first opened a regular Minecraft game, and I played around to figure out what angle the camera should look at to be able to mine down in a staircase.
After that, I was able to write a script that mostly worked correctly, and I refined it through testing.

## Performance
The scripted solution resulted in the agent successfully mining stone in **9/10** tests. The failed test was due to spawning on a desert island. The first few blocks were just sand, and then the agent mined out into the ocean where it drowned. Additionally, the agent failed to climb out of its hole in another test where it fell into a cave. These are the downsides of scripting—the solution is not adaptable—however, overall, I would say the performance was quite good.

The exact reward for each test was [21, 19, 22, 11, 23, 19, 0, 19, 24, 18].

## Links
The script can be found at [scripted_stone_collection.py]().

The video can be found at [scripted_stone_collection_demo.mp4]().