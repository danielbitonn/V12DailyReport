import json
import threading
from datetime import datetime as dt
import os
import getpass
import socket
import copy

def func_remove_symbols(input_string):
    return ''.join(char.lower() for char in input_string if char.isalnum())
class conf:
    def __init__(self):
        self.METADATA_FLAG          = 0
        # Attributes
        self.VERSION                = "V112"
        self.METADATA_DATE          = "2023-08-07"
        self.DT_FORMAT              = "%Y-%m-%d"
        self.T_FORMAT               = "%H:%M"
        self.DT_YYYY_MM_DD__HH_MM   = f"{self.DT_FORMAT }__{self.T_FORMAT}"
        self.METADATA_TODAY         = dt.now().strftime(f'{self.DT_FORMAT}')
        self.ROOT_PATH              = "output"
        self.FILES_PATH             = "files"
        self.IMAGES_PATH            = "images"
        self.DATA_PATH              = "data"
        self.LOG_PATH               = "log"
        self.FILES_PATH_FULL        = f"{self.ROOT_PATH}\\{self.FILES_PATH}"
        self.IMAGES_PATH_FULL       = f"{self.ROOT_PATH}\\{self.IMAGES_PATH}"
        self.DATA_PATH_FULL         = f"{self.ROOT_PATH}\\{self.DATA_PATH}"
        self.LOG_PATH_FULL          = f"{self.ROOT_PATH}\\{self.LOG_PATH}"
        self.LOG_FATAL_ERRORS       = []
        self.LOG_DAYS_TO_DELETE     = 1
        self.LOG_PREFIX             = "log__"
        self.LOG_T_FORMAT           = '%H-%M'
        self.LOG_YYYY_MM_DD__HH_MM  = f"{self.DT_FORMAT }__{self.LOG_T_FORMAT}"
        self.ROOT_README_FILE_NAME  = "README.txt"
        self.AZK                    = "DefaultEndpointsProtocol=https;AccountName=v12daily;AccountKey=2tBxBHZwM5WNyzPAyozRtsircGCFBAMN2S3TfZGFN923bIlkWAjdn5scM5vV5TkYPFKvukfD/cL5+AStMluGag==;EndpointSuffix=core.windows.net"
        self.LOCAL_MACHINE          = func_remove_symbols(socket.gethostname())
        self.USER                   = getpass.getuser()
        # Dictionary
        self.DEFAULT_DICT           = self.set_conf_dict()
        self.REF_META               = {}
        self.META                   = {}
        # Inherent params
        self.lock = threading.Lock()  # Add a lock attribute to the class
        self.conf_read_or_write_meta_data_json()

    def set_attribute(self, key, value):
        with self.lock:  # Use the lock when setting attributes
            self.META[key] = value
    def get_attribute(self, key):
        with self.lock:  # Use the lock when setting attributes
            return self.META.get(key, None)
    def set_conf_dict(self):
        tmp_dict = {"METADATA":{}}
        for k, v in self.__dict__.items():
            tmp_dict["METADATA"][k] = v
        return tmp_dict

    def conf_read_or_write_meta_data_json(self):
        # Function to write the default metadata
        path = "./src/metadata/METADATA_CONF.json"
        def write_default_metadata():
            with open(path, 'w') as f:
                json.dump(self.DEFAULT_DICT, f, indent=4)
            return self.DEFAULT_DICT["METADATA"]

        # Check if the file exists
        if os.path.exists(path):
            with open(path, 'r') as file:
                meta_data = json.load(file)
            # Check the METADATA_FLAG
            if meta_data["METADATA"]["METADATA_FLAG"]:
                result = meta_data["METADATA"]
            else:
                result = write_default_metadata()
        else:
            result = write_default_metadata()
        self.REF_META = copy.deepcopy(result)
        self.META = result
        # return result


DMD = conf()
DMDD = DMD.META
