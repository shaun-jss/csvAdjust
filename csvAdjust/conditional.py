import logging
from enum import Enum
from abc import ABC, abstractmethod

class FieldType(Enum):
    """Enumeration of the valid kinds of required fields a conditional can have"""
    COLUMN_NUMBER = ("columnnumber")
    VALUE = ("value")
    
    def __init__(self, jsonName):
        self.jsonName = jsonName
        
class Conditional(ABC):
    """Abstract class that concrete conditional classes extend. This might not be that necessary, but my day job
    is Java development, and I feel the need to make an interface even in Python."""

    @abstractmethod
    def is_met(self, row):
        """"Child classes have to implements this method. When called, the conditional checks if it is met or not.
        NOTE: The row object is 0-indexed
        """
        pass
    
    @classmethod
    @abstractmethod
    def get_required_fields(cls):
        """This method will return the fields required by the conditional"""
        
    @staticmethod
    def parse_conditionals(conditional_list):
        """Takes a list of dictionaries that contain conditional configurations and transforms them into conditional objects"""
        conditionals = []
        for condition in conditional_list:
            conType = ConditionalType.get_type(condition['type'])
            
            # If we can't figure out the type, throw an exception to prevent unintended wonky stuff from happening in the output files
            if conType is None:
                logging.error("Unable to determine conditional type '%s'. Available conditional types are '%s'", 
                              condition['type'], ', '.join(str(e.jsonName) for e in conTypes))
                
                raise Exception("Unable to determine conditional type")
            
            # Get the required fields of this condition
            requiredFields = conType.implementation.get_required_fields()
            
            # Now lets get the fields from the configuration
            fieldValues = []
            for field in requiredFields:
                # Throw an exception if a required field is missing
                if field.jsonName not in condition:
                    logging.error("Unable to find required field '%s' for a '%s' condition",
                                  field.jsonName, conType.name)
                    raise Exception("Missing required field for conditional")
                
                fieldValues.append(condition[field.jsonName])
                
            # Now lets actually create the conditional objects. 
            # We can pass in the values stored in the fieldValues list as arguments to the constructor by unpacking the list
            # We do that by putting a * in front of the variable name
            conditionals.append(conType.implementation(*fieldValues))  
            
        return conditionals
                
    
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
    
    @classmethod
    def get_required_fields(cls):
        return (FieldType.COLUMN_NUMBER, FieldType.VALUE)
    
class ColumnContains(Conditional):
    """Checks if a column contains a value"""
    
    def __init__(self, columnNumber, value):
        self.columnNumber = columnNumber
        self.value = value
        
    def is_met(self, row):
        """"Checks if column contains the value
        
        Parameters
        ----------
        row : list
            The values of an entire row in a CSV. Each element is a different column
        """
        return self.value in row[self.columnNumber]
    
    @classmethod
    def get_required_fields(cls):
        return (FieldType.COLUMN_NUMBER, FieldType.VALUE)
    
class RowContains(Conditional):
    """Checks if a value exists in any of the columns"""
    
    def __init__(self, value):
        """We don't actually need columnNumber, but it is included to follow the patter"""
        self.value = value
         
    def is_met(self, row):
        """"Checks if the value exists anywhere in this row
        
        Parameters
        ----------
        row : list
            The values of an entire row in a CSV. Each element is a different column
        """
        for column in row:
            if self.value in column:
                return True
            
        return False
    
    @classmethod
    def get_required_fields(cls):
        return (FieldType.VALUE,)
    
class ConditionalType(Enum):
    """The types of conditionals that can be used"""
    
    COLUMN_EQUALS = ("columnequals", ColumnEquals)
    COLUMN_CONTAINS = ("columncontains", ColumnContains)
    ROW_CONTAINS = ("rowcontains", RowContains)
    

    def __init__(self, jsonName, implementation):
        self.jsonName = jsonName
        self.implementation = implementation
        
    @classmethod
    def get_type(cls, name):
        """Returns the ConditionalType that matches the string passed in"""
        for conditional in cls:
            if conditional.jsonName is name:
                return conditional
            
        return None