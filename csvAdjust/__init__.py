from enum import Enum

class CSVAdjustFieldType(Enum):
    """Enumeration of the valid kinds of required fields a conditional can have"""
    COLUMN_NUMBER = ("columnnumber")
    VALUE = ("value")
    
    def __init__(self, jsonName):
        self.jsonName = jsonName