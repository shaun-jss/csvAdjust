import logging
from enum import Enum
from abc import ABC, abstractmethod

class Conditional(ABC):
    """Abstract class that concrete conditional classes extend. This might not be that necessary, but my day job
    is Java development, and I feel the need to make an interface even in Python."""

    @abstractmethod
    def is_met(self, row):
        """"Child classes have to implements this method. When called, the conditional checks if it is met or not.
        NOTE: The row object is 0-indexed
        """
        pass
    
class ColumnEquals(Conditional):
    """Checks for column equality to a predetermined value"""
    
    def __init__(self, columnNumber, value):
        """Creates a ColumnEquals conditional
        
        Parameters
        ----------
        columnNumber : int
            The column number to check. This value is 0-indexed
        value :
            What we are checking the column's value against
        """
        self.columnNumber = columnNumber
        self.value = value
    
    def is_met(self, row):
        """"Checks the column equality
        
        Parameters
        ----------
        row : list
            The values of an entire row in a CSV. Each element is a different column
        """
        return row[self.columnNumber] == self.value
    
class ColumnContains(Conditional):
    """Checks if a column contains a value"""
    
    def __init__(self, columnNumber, value):
        self.columnNumber = columnNumber
        self.value = value
        
    def is_met(self, row):
        """Checks if the value is in the column"""
        return self.value in row[self.columnNumber]
    
class RowContains(Conditional):
    """Checks if a value exists in any of the columns"""
    
    def __init__(self, columnNumber, value):
        """We don't actually need columnNumber, but it is included to follow the patter"""
        self.columnNumber = columnNumber
        self.value = value
         
    def is_met(self, row):
        for column in row:
            if self.value in column:
                return True
            
        return False
    
class ConditionalTypes(Enum):
    """The types of conditionals that can be used"""
    
    COLUMN_EQUALS = ("Column Equals", "columnequals", ColumnEquals)
    COLUMN_CONTAINS = ("Column Contains", "columncontains", ColumnContains)
    ROW_CONTAINS = ("Row Contains", "rowcontains", RowContains)

    def __init__(self, id, jsonName, implementation):
        self.id = id
        self.jsonName = jsonName
        self.implementation = implementation