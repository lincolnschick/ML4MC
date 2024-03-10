"""
Author: Adair Torres
Description:
    Model object file to represent individual models.
Last Modified: 1-28-2024
"""

import os

class Model:
    def __init__(self, name, obj, path):
        self._name = name
        self._objective = obj
        self._FILEPATH = path

    def get_name(self):
        return self._name
    
    def get_filepath(self):
        return self._FILEPATH
    
    def get_objective(self):
        return self._objective