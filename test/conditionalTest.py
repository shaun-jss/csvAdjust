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
        
        contains = conditional.RowContains("urp")
        
        self.assertTrue(contains.is_met(row))
        
        row[5] = "White"
        
        self.assertFalse(contains.is_met(row))
        
    def test_conditional_types_enum(self):
        """Tests for the ConditionalType enumeration"""
        conTypes = conditional.ConditionalType
        
        self.assertEqual(3, len(conTypes))
        
        self.assertEqual(conTypes.get_type("columnequals"), conTypes.COLUMN_EQUALS)
        self.assertEqual(conTypes.get_type("columncontains"), conTypes.COLUMN_CONTAINS)
        self.assertEqual(conTypes.get_type("rowcontains"), conTypes.ROW_CONTAINS)
        
    def test_conditional_parsing(self):
        testConfig = [
            {
                "type":"columnequals",
                "columnnumber":2,
                "value":"whatever"
            },
            {
                "type":"columncontains",
                "columnnumber":7,
                "value":9.2
            },
            {
                "type":"rowcontains",
                "value":"Mango"
            }
        ]
        
        conditionals = conditional.Conditional.parse_conditionals(testConfig)
        
        # Verify the correct amount were created
        self.assertEqual(len(conditionals), 3)
        
        # Verify the correct objects where created
        conTypes = conditional.ConditionalType
        
        self.assertEqual(type(conditionals[0]), conTypes.COLUMN_EQUALS.implementation)
        self.assertEqual(type(conditionals[1]), conTypes.COLUMN_CONTAINS.implementation)
        self.assertEqual(type(conditionals[2]), conTypes.ROW_CONTAINS.implementation)
        
        #Missing required field value
        brokeConfig = [
            {
                "type":"columnequals",
                "columnnumber":2
            }
        ]
        self.assertRaises(Exception, callable)
        

    @staticmethod
    def get_default_list():
        return ["Red", "Green", "Blue", "Yellow", "Orange", "Purple"]
    
    @classmethod
    def make_list(cls, numberOfElements, values=[""]):
        list = []
        for i in range(numberOfElements):
            list.append(values[i % len(values)])
            
        return list