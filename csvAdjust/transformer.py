import logging
from enum import Enum
from abc import ABC, abstractmethod
from . import CSVAdjustFieldType

class OperationType(Enum):
    """Operation types supported"""
    REPLACE = ("replace")
    ADD = ("add")
    SUBTRACT = ("subtract")
    APPEND = ("append")
    
    def __init__(self, jsonName):
        self.jsonName = jsonName
        
class Transformer(ABC):
    """Abstract class that concrete transformer classes extend."""
    
    @abstractmethod
    def transform(self, row):
        """This method is called to make the change to the row"""
        pass
    
    @classmethod
    @abstractmethod
    def get_required_fields(cls):
        """This method will return the fields required to instantiate the transformer"""

class NumberTransformer(Transformer, ABC):
    """Class that all arithmetic transformations inherit."""
    
    def __init__(self, columnNumber, value):
        """Creates a number transformer object
        
        Parameters
        ----------
        columnNumber : int
            The column number to target
        value
            The value to perform the operation on
        """
        self.columnNumber = columnNumber
        self.value = value
        
    def transform(self, row):
        if not type(row[self.columnNumber]) is int:# or not type(row[self.columnNumber]) is float:
            logging.error("Unable to add '%d' to '%s'", self.value, row[self.columnNumber])
            raise Exception("Cannot add value to non number types")
        
    @classmethod
    def get_required_fields(cls):
        return (CSVAdjustFieldType.COLUMN_NUMBER, CSVAdjustFieldType.VALUE)

class StringTransformer(Transformer, ABC):
    """Class that all string transformations inherit."""
    
    def __init__(self, columnNumber, value):
        """Creates a string transformer object
        
        Parameters
        ----------
        columnNumber : int
            The column number to replace
        value
            The value to set the cell to
        """
        self.columnNumber = columnNumber
        self.value = value
        
    @classmethod
    def get_required_fields(cls):
        return (CSVAdjustFieldType.COLUMN_NUMBER, CSVAdjustFieldType.VALUE)
        
class Replace(StringTransformer):
    """Replaces the value of a cell with another value"""
        
    def transform(self, row):
        """Replaces the value in the column specified with the value requested"""
        row[self.columnNumber] = self.value
    
class Append(StringTransformer):
    """Appends the value of a cell with another value"""
        
    def transform(self, row):
        """Appends the value requested to the value in the column specified"""
        row[self.columnNumber] = str(row[self.columnNumber]) + str(self.value)
        
class Add(NumberTransformer):
    """Adds the requested value to the value of the cell. This will raise an exception if the cell
    is not a number type"""
        
    def transform(self, row):
        """Adds the value in the cell specified with the value requested
        
        Raises
        ------
        
        Exception
            If the cell's value does not contain a number
        """
        super().transform(row)
        row[self.columnNumber] = row[self.columnNumber] + self.value
    
class Subtract(NumberTransformer):
    """Subtracts the requested value to the value of the cell. This will raise an exception if the cell
    is not a number type"""
        
    def transform(self, row):
        """Subtracts the value in the cell specified with the value requested
        
        Raises
        ------
        
        Exception
            If the cell's value does not contain a number
        """
        super().transform(row)
        row[self.columnNumber] = row[self.columnNumber] - self.value