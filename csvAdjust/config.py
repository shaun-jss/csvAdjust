import json, os, logging
from enum import Enum


def lower_case_all_keys(lower_keys):
    """Helper method to lower case all the keys in the dictionary"""
    #Handle lists/arrays
    if type(lower_keys) is list:
        new_list = []
        for value in lower_keys:
            new_list.append(lower_case_all_keys(value))

        return new_list

    #Handle dictionaries
    if type(lower_keys) is dict:
        new_dict = dict()
        for key, value in lower_keys.items():
            if type(value) is dict or list:
                value = lower_case_all_keys(value)

            new_dict[key.lower()] = value

        return new_dict

    #It wasn't a list or dictionary, so just return it
    return lower_keys
    


class ConfigSection(Enum):
    """Enumeration defining different sections in the config file"""
    ROOT = ("Root", None, "", None)
    
    #Logging section
    LOGGING = ("Logging", ROOT[0], "logging", None)
    LOG_FILENAME = ("Log Filename", LOGGING[0], "filename", "adjuster.log")
    LOG_ENCODING = ("Log Encoding", LOGGING[0], "encoding", "utf-8")
    LOG_LEVEL = ("Log Level", LOGGING[0], "level", "INFO")
    LOG_FORMAT = ("Log Format", LOGGING[0], "format", "%(levelname)s %(message)s")
    LOG_FILE_MODE = ("Log File Mode", LOGGING[0], "filemode", "a")

    #CSV section
    CSVS = ("CSVs", ROOT[0], "csvs", [])
    READ_DIRECTORY = ("Read Directory", CSVS[0], "readdirectory", os.path.join(os.getcwd(), "original"))
    WRITE_DIRECTORY = ("Write Directory", CSVS[0], "writedirectory", os.path.join(os.getcwd(), "changed"))
    FILE_ENCODING = ("File Encoding", CSVS[0], "fileencoding", "utf-8")
    REMOVE_FILES_IN_WRITE_DIRECTORY = ("Remove Files In Write Directory", CSVS[0], "removefilesinwritedirectory", False)
    DIALECT = ("Dialect", CSVS[0], "dialect", "excel")

    def __init__(self, id, parentSection, jsonName, defaultValue):
        self.id = id
        self.parentSection = parentSection
        self.jsonName = jsonName
        self.defaultValue = defaultValue

    @classmethod
    def getChildSections(cls, parent):
        """Returns a list of all the sections that are directly under a parent section"""
        ret_list = []
        for child in cls:
            if child.parentSection is parent.id:
                ret_list.append(child)

        return ret_list

class CSVAdjustConfig(object):
    """
    The basic object for loading and managing the configuartion
    of the entire application.
    """

    #Default file name that will be loaded if one is not passed in
    __DEFAULT_CONFIG_FILENAME = 'csvAdjuster.json'

    def __init__(self, fileName=__DEFAULT_CONFIG_FILENAME, path=None):
        """Loads the configuation for the application run.

        Parameters
        ----------
        fileName : str
            The file name to load the configuation from
        path : str
            The file path to look for the file name in
        """
        #Load the file
        self._load_file(fileName, path)

        #Get logging setup so we can tell the user stuff
        self._setup_logging()

    def get_config_dict(self):
        """Getter for the underlying dictionary"""
        return self.__config

    def _setup_logging(self):
        """Sets up the logging module for the task run"""
        self._verify_logging_section()

        #I just want this so I don't have to type as much
        logConfig = self.__config[ConfigSection.LOGGING.jsonName]
        logging.basicConfig(
            filename=logConfig[ConfigSection.LOG_FILENAME.jsonName],
            encoding=logConfig[ConfigSection.LOG_ENCODING.jsonName],
            level=logConfig[ConfigSection.LOG_LEVEL.jsonName],
            format=logConfig[ConfigSection.LOG_FORMAT.jsonName],
            filemode=logConfig[ConfigSection.LOG_FILE_MODE.jsonName]
        )

        logging.info("Loading configuration from %s", self.configPath)

    def _load_file(self, fileName, path):
        """Loads the configuration file from the file system
        
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
            raw_dict = json.loads(json_data)
            
            #Make all the keys lowercase
            self.__config = lower_case_all_keys(raw_dict)

    def _verify_logging_section(self):
        """Verifies that the logging section has either has a configuration property, or has the default value"""
        if not ConfigSection.LOGGING.jsonName in self.__config:
            self.__config[ConfigSection.LOGGING.jsonName] = dict()

        for child in ConfigSection.getChildSections(ConfigSection.LOGGING):
            if child.jsonName not in self.__config[ConfigSection.LOGGING.jsonName] and child.defaultValue is not None:
                self.__config[ConfigSection.LOGGING.jsonName] = child.defaultValue
