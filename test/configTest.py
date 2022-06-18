import unittest, os

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
        adjustConfig = config.CSVAdjustConfig()
        adjustConfig.load_config(fileName=fileName, path=CSVAdjustConfigTest.__TEMP_PATH)

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
            adjustConfig.load_config()
        finally:
            os.remove(os.path.join(cwd, defaultFileName))

        
    @classmethod
    def setUpClass(cls):
        """Creates the temp directory to use"""
        cwd = os.getcwd()
        
        CSVAdjustConfigTest.__TEMP_PATH = os.path.join(cwd, "configTestTempDir")

        if not os.path.exists(CSVAdjustConfigTest.__TEMP_PATH):
            os.makedirs(CSVAdjustConfigTest.__TEMP_PATH)
    
    @classmethod
    def tearDownClass(cls):
        for file in os.listdir(CSVAdjustConfigTest.__TEMP_PATH):
            os.remove(os.path.join(CSVAdjustConfigTest.__TEMP_PATH, file))

        os.removedirs(CSVAdjustConfigTest.__TEMP_PATH)

    @classmethod
    def get_test_json_string(cls):
        """Returns a json string that can be used for testing"""

        return """{
            "csv":
            [
                {
                    "readDirectory":"somePlace",
                    "wirteDirectory":"someOtherPlace",
                    "fileEncoding":"utf-8",
                    "dialect":"excel"
                }
            ]
        }
        """

if __name__ == '__main__':
    unittest.main()