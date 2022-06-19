import unittest

from csvAdjust import transformer

class TransformerTest(unittest.TestCase):
    """Tests for the transformer implementations"""
    
    def test_add_transformer(self):
        """Tests the add transformer"""
        row = TransformerTest.get_default_number_list()
        
        add = transformer.Add(2, 6)
        add.transform(row)
        
        self.assertEqual(row[2], 11)
        
        with self.assertRaises(Exception):
            add.transform(TransformerTest.get_default_color_list())
            
        self.assertEqual(len(transformer.Add.get_required_fields()), 2)
        
    def test_subtract_transformer(self):
        """Tests the subtract transformer"""
        row = TransformerTest.get_default_number_list()
        
        sub = transformer.Subtract(1, 21)
        sub.transform(row)
        
        self.assertEqual(row[1], 100)
        
        with self.assertRaises(Exception):
            sub.transform(TransformerTest.get_default_color_list())
            
        self.assertEqual(len(transformer.Subtract.get_required_fields()), 2)
        
    def test_replace_transformer(self):
        """Tests the replace transformer"""
        row = TransformerTest.get_default_color_list()
        
        replace = transformer.Replace(1, "White")
        replace.transform(row)
        
        self.assertEqual(row[1], "White")
        
        row = TransformerTest.get_default_number_list()    
        replace.transform(row)
        
        self.assertEqual(row[1], "White")
        
    def test_append_transformer(self):
        """Tests the append transformer"""
        row = TransformerTest.get_default_color_list()
        
        append = transformer.Append(1, "Black")
        append.transform(row)
        
        self.assertEqual(row[1], "GreenBlack")
        
        row = TransformerTest.get_default_number_list()    
        append.transform(row)
        
        self.assertEqual(row[1], "121Black")
        
    @staticmethod
    def get_default_color_list():
        return ["Red", "Green", "Blue", "Yellow", "Orange", "Purple"]
    
    @staticmethod
    def get_default_number_list():
        return [100, 121, 5, 1000, 17, 13]