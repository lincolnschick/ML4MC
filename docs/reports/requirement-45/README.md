# Requirement 45 

[Crafting Script Demo](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-45/crafting_script_demo.mov)

From the artifact:
Successful completion of this artifact includes:
- Presenting new models for chopping trees, collecting stone, and mining iron with crafting implemented.
    - See [stone_model.pth](https://github.com/lincolnschick/ML4MC/blob/8c2f77c64537dd906ffdd899048507e067375afd/src/GUI/models/stone_model.pth) and [iron_model.pth](https://github.com/lincolnschick/ML4MC/blob/8c2f77c64537dd906ffdd899048507e067375afd/src/GUI/models/iron_model.pth) for the models. It was impossible to train the tree model with crafting as the tree chop dataset only included POV observations; no data for crafting/equipping actions was available.
- Presenting scripts for creating common tools: wooden pickaxe, wooden sword, stone pickaxe, stone sword, iron pickaxe, crafting table, and furnace.
    - All scripts were combined to either crafting swords or pickaxes. The best sword/pickaxe would be crafted based on the materials available.
    - See [crafting_scripts.py](https://github.com/lincolnschick/ML4MC/blob/8c2f77c64537dd906ffdd899048507e067375afd/src/scripts/crafting_scripts.py) for all of these scripts.
- Presenting scripts for smelting iron ore.
    - See [smelt_iron](https://github.com/lincolnschick/ML4MC/blob/8c2f77c64537dd906ffdd899048507e067375afd/src/scripts/crafting_scripts.py#L107). This is a helper script in the crafting_scripts.py file.
