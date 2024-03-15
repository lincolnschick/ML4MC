# Requirement 43
[Demo](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-43/gather_stone_demo.mov)

From the artifact
Successful completion of this script includes:
- Centering the agent prior to mining down (to ensure it works regardless of the agent's position)
    - See [here](https://github.com/lincolnschick/ML4MC/blob/d429be4ed6becd77e2491749ff8ec9332a202460/src/scripts/gather_stone.py#L44C4-L44C39)
- Detecting broken pickaxes and equipping a new one if available
    - See [here](https://github.com/lincolnschick/ML4MC/blob/d429be4ed6becd77e2491749ff8ec9332a202460/src/scripts/gather_stone.py#L56) and [here](https://github.com/lincolnschick/ML4MC/blob/765147ed27434c41032400d07d7179d884ff008d/src/scripts/gather_stone.py#L75)
- Mining stone in a loop until the user terminates
    - See [here](https://github.com/lincolnschick/ML4MC/blob/d429be4ed6becd77e2491749ff8ec9332a202460/src/scripts/gather_stone.py#L74)
- Using the agent's Y-coordinate to determine how deep to mine down before continuing in a line
    - See [here](https://github.com/lincolnschick/ML4MC/blob/d429be4ed6becd77e2491749ff8ec9332a202460/src/scripts/gather_stone.py#L53)