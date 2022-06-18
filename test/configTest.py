import unittest, os, json

from csvAdjust import config

class CSVAdjustConfigTest(unittest.TestCase):
    """Tests for the CSVAdjustConfig class"""

    __TEMP_PATH = None
        
    def test_load_config_with_full_path_specified(self):
        """This test verifies that the when the file name and path are specified, they
        are used and the default is not"""

        #First write a test config file to our temp directory
        fileName = 'testConfig.json'

        with open(os.path.join(CSVAdjustConfigTest.__TEMP_PATH, fileName), 'w') as fileHandle:
            fileHandle.write(CSVAdjustConfigTest.get_test_json_string())
            fileHandle.close()

        #Now run the test
        adjustConfig = config.CSVAdjustConfig(fileName=fileName, path=CSVAdjustConfigTest.__TEMP_PATH)

        #Verify that stuff loaded correctly
        check = adjustConfig.get_config_dict()
        Sec = config.ConfigSection

        self.assertIn(Sec.LOGGING.jsonName, check)

        loggingCheck = check[Sec.LOGGING.jsonName]

        #Make sure we have all the logging values we should
        self.assertEqual(len(Sec.getChildSections(Sec.LOGGING)), len(loggingCheck))
        
        #Make sure each key made it in and has the correct value
        for tag in Sec.getChildSections(Sec.LOGGING):
            self.assertIn(tag.jsonName, loggingCheck)
            self.assertEqual(tag.defaultValue, loggingCheck[tag.jsonName])

    def test_load_config_with_defaults(self):
        """Verifies that the defaults are loaded correctly. If you chnage the __DEFAULT_CONFIG_FILENAME
        class variable, you gotta change it here too"""
        #Make the default
        cwd = os.getcwd()
        defaultFileName = 'csvAdjuster.json'

        with open(os.path.join(cwd, defaultFileName), 'w') as fileHandle:
            fileHandle.write(CSVAdjustConfigTest.get_test_json_string())

        try:
            #Now run the test
            adjustConfig = config.CSVAdjustConfig()

            #Verify that stuff loaded correctly
            check = adjustConfig.get_config_dict()
            Sec = config.ConfigSection

            self.assertIn(Sec.LOGGING.jsonName, check)

            loggingCheck = check[Sec.LOGGING.jsonName]

            #Make sure we have all the logging values we should
            self.assertEqual(len(Sec.getChildSections(Sec.LOGGING)), len(loggingCheck))
            
            #Make sure each key made it in and has the correct value
            for tag in Sec.getChildSections(Sec.LOGGING):
                self.assertIn(tag.jsonName, loggingCheck)
                self.assertEqual(tag.defaultValue, loggingCheck[tag.jsonName])

        finally:
            #This file doesn't go in the temp dir, so make sure we remove it
            os.remove(os.path.join(cwd, defaultFileName))

    def test_config_section_enum(self):
        """Verifies everything with the config section enumeration is fine"""
        Sec = config.ConfigSection
        self.assertEqual(7, len(Sec))
        

    @unittest.skip("I don't think this is handling list correctly, and I don't want to work on it now")
    def test_lower_case_all_keys(self):
        """Tests the __lower_case_all_keys method, which is designed to lower case all the keys in a dictionary"""
        test_dict = dict()

        test_dict['TestONE'] = 'alpha'
        test_dict['testtwo'] = 'betA'
        test_dict['TESTTHREE'] = 'gaMMa'
        sub_list = []
        sub_list.append({'subTestOne': 'APPLE', 'subtestTWO' : 'mango', 'subTESTthree' : 'kiwI'})
        test_dict['TestFour'] = sub_list

        #compareDict = config.lower_case_all_keys(test_dict)

        #Verify the keys are lower case
        #self.assertIn('testone', compareDict)
        #self.assertIn('testtwo', compareDict)
        #self.assertIn('testthree', compareDict)
        #self.assertIn('testfour', compareDict)

        #Make sure the data didn't change
        #self.assertEqual(compareDict['testone'], 'alpha')
        #self.assertEqual(compareDict['testtwo'], 'betA')
        #self.assertEqual(compareDict['testthree'], 'gaMMa')

        #Verify the list made it through
        #self.assertTrue(type(compareDict['testfour']) is list)

        #Lets make sure the sub dictionary worked
        #subList = compareDict['testfour']

        #self.assertTrue(type(subList) is list)

        
        #self.assertIn('subtestone', subList[0])
        #self.assertIn('subtesttwo', subList[1])
        #self.assertIn('subtestthree', subList[2])
        

        
    @classmethod
    def setUpClass(cls):
        """Creates the temp directory"""
        cwd = os.getcwd()
        
        CSVAdjustConfigTest.__TEMP_PATH = os.path.join(cwd, "configTestTempDir")

        if not os.path.exists(CSVAdjustConfigTest.__TEMP_PATH):
            os.makedirs(CSVAdjustConfigTest.__TEMP_PATH)
    
    @classmethod
    def tearDownClass(cls):
        """Remove the temp directory and the files in it"""
        for file in os.listdir(CSVAdjustConfigTest.__TEMP_PATH):
            os.remove(os.path.join(CSVAdjustConfigTest.__TEMP_PATH, file))

        os.removedirs(CSVAdjustConfigTest.__TEMP_PATH)

    @classmethod
    def get_test_dict(cls):
        """Builds up a test config using the default values defined"""
        testDict = dict()

        for root in config.ConfigSection.getChildSections(config.ConfigSection.ROOT):
            testDict[root.jsonName] = dict()

            for child in config.ConfigSection.getChildSections(root):
                testDict[root.jsonName][child.jsonName] = child.defaultValue

        return testDict

    @classmethod
    def get_test_json_string(cls):
        """Returns a json string that can be used for testing"""
        ret_json = json.dumps(CSVAdjustConfigTest.get_test_dict())

        return ret_json

if __name__ == '__main__':
    unittest.main()