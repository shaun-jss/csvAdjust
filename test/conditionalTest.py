import unittest

from csvAdjust import conditional

class ConditionalTest(unittest.TestCase):
    """Tests for the conditional implementations"""
    
    def test_column_equals(self):
        """Tests the column equals conditional"""
        row = ConditionalTest.get_default_list()
        
        equals = conditional.ColumnEquals(2, "Blue")
        
        self.assertTrue(equals.is_met(row))
        
        row[2] = "Black"
        
        self.assertFalse(equals.is_met(row))
        
    def test_column_contains(self):
        """Tests the column contains conditional"""
        row = ConditionalTest.get_default_list()
        
        contains = conditional.ColumnContains(3, "ello")
        
        self.assertTrue(contains.is_met(row))
        
        row[3] = "Grey"
        
        self.assertFalse(contains.is_met(row))
        
    def test_row_contains(self):
        """Tests the row contains conditional"""
        row = ConditionalTest.get_default_list()
        
        contains = conditional.RowContains(None, "urp")
        
        self.assertTrue(contains.is_met(row))
        
        row[5] = "White"
        
        self.assertFalse(contains.is_met(row))

    @staticmethod
    def get_default_list():
        return ["Red", "Green", "Blue", "Yellow", "Orange", "Purple"]
    
    @classmethod
    def make_list(cls, numberOfElements, values=[""]):
        list = []
        for i in range(numberOfElements):
            list.append(values[i % len(values)])
            
        return list