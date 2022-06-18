import json, os

class CSVAdjustConfig(object):
    """
    The basic object for loading and managing the configuartion
    of the entire application.
    """

    #Default file name that will be loaded if one is not passed in
    __DEFAULT_CONFIG_FILENAME = 'csvAdjuster.json'

    def __init__(self):
        pass

    def load_config(self, fileName=__DEFAULT_CONFIG_FILENAME, path=None):
        """Loads the configuation for the application run.

        Parameters
        ----------
        fileName : str
            The file name to load the configuation from
        path : str
            The file path to look for the file name in
        """
        self.path = path
        self.fileName = fileName

        #If a path isn't passed in, just use the current working directory
        if self.path is None:
            self.path = os.getcwd()

        self.configPath = os.path.join(self.path, fileName)

        if not os.path.isfile(self.configPath):
            #The path isn't a file, so throw an exception
            raise Exception(self.configPath + ' is not a file')

        #Load the configuration
        with open(self.configPath, 'r') as file_handle:
            json_data = file_handle.read()

            self.__config = json.loads(json_data)