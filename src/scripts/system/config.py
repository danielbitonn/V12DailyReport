from datetime import datetime as dt, timedelta as td
import threading
import os
import glob
import json
import getpass
import socket
import copy
from src.scripts.cloud.azure_interface import func_initial_azure
def func_remove_symbols(input_string):
    return ''.join(char.lower() for char in input_string if char.isalnum())
def folders_handler(path):
    if not os.path.exists(path):
        os.makedirs(path)
def colors_dict_to_tuples(color_dict):
    # Mapping between color codes and names
    color_name_mapping = {
        "#ccffcc": "lightgreen",
        "#ffe6cc": "lightorange",
        "#ffffcc": "lightyellow",
        "#e6ccff": "lightpurple",
        "#ffcccc": "red",
        "#999900": "darkyellow",
        "#87CEFA": "lightskyblue",
        "#9370DB": "mediumorchid",
        "#BC0E00": "darkred",
        "#EBB517": "goldenrod",
        "#FFD700": "gold",
        "#90EE90": "lightgreen",
        "#008000": "green",
        "#0000FF": "blue",
        "#20B2AA": "lightseagreen",
        "#778899": "lightslategray",
        "#FF8C00": "darkorange",
        "#FF4500": "orangered",
        "#2E8B57": "seagreen",
        "#6B8E23": "olivedrab",
        "#8B4513": "saddlebrown",
        "#D2B48C": "tan",
        "#D8BFD8": "thistle",
        "#FA8072": "salmon",
        "#F5DEB3": "wheat",
        "#C71585": "mediumvioletred"
    }
    result = []
    for status, color_code in color_dict.items():
        color_name = color_name_mapping.get(color_code, "black")
        result.append((status, color_name, color_code))
    return result
def auto_func_delete_old_files():
    cutoff = dt.now() - td(days=DMDD["LOG_DAYS_TO_DELETE"])
    log_files = glob.glob(f'{DMDD["LOG_PATH_FULL"]}\\{DMDD["LOG_PREFIX"]}*')
    for log_file in log_files:
        date_str = log_file.split('__')[2]                                                                              # Extract date from filename
        file_date = dt.strptime(date_str, DMDD['DT_FORMAT'])
        if file_date < cutoff:                                                                                          # If file is older than X days, delete it
            os.remove(log_file)
            DMDD["DELETED_FILES"].append(log_file)
    return DMDD["DELETED_FILES"]
class conf:
    def __init__(self):
        self.METADATA_FLAG          = 0
        ### Attributes ###
        self.VERSION                                = "V115"
        self.METADATA_DATE                          = "2023-08-07"
        self.DT_FORMAT                              = "%Y-%m-%d"
        self.T_FORMAT                               = "%H:%M"
        self.DT_YYYY_MM_DD__HH_MM                   = f"{self.DT_FORMAT }__{self.T_FORMAT}"
        self.METADATA_TODAY                         = dt.now().strftime(f'{self.DT_FORMAT}')
        self.ROOT_PATH                              = "output"
        self.FILES_PATH                             = "files"
        self.IMAGES_PATH                            = "images"
        self.DATA_PATH                              = "data"
        self.LOG_PATH                               = "log"
        self.FILES_PATH_FULL                        = f"{self.ROOT_PATH}\\{self.FILES_PATH}"
        self.IMAGES_PATH_FULL                       = f"{self.ROOT_PATH}\\{self.IMAGES_PATH}"
        self.DATA_PATH_FULL                         = f"{self.ROOT_PATH}\\{self.DATA_PATH}"
        self.LOG_PATH_FULL                          = f"{self.ROOT_PATH}\\{self.LOG_PATH}"
        self.LOG_DAYS_TO_DELETE                     = 1
        self.LOG_FATAL_ERRORS                       = []
        self.DELETED_FILES                          = []
        self.LOG_PREFIX                             = "log__"
        self.LOG_T_FORMAT                           = "%H-%M"
        self.LOG_YYYY_MM_DD__HH_MM                  = f"{self.DT_FORMAT }__{self.LOG_T_FORMAT}"
        self.ROOT_README_FILE_NAME                  = "README.txt"
        self.AZK                                    = "DefaultEndpointsProtocol=https;AccountName=v12daily;AccountKey=2tBxBHZwM5WNyzPAyozRtsircGCFBAMN2S3TfZGFN923bIlkWAjdn5scM5vV5TkYPFKvukfD/cL5+AStMluGag==;EndpointSuffix=core.windows.net"
        self.CONF_CONTAINER_NAME                    = "dbs"
        self.LOCAL_MACHINE                          = func_remove_symbols(socket.gethostname())
        self.USER                                   = getpass.getuser()
        self.ANIMATION_OR_PICTURE_FLAG              = 1                                                                              # Animation or picture
        self.CHECK_QUEUE_FREQ                       = 100
        self.METADATA_PATH                          = "./src/metadata/METADATA_CONF.json"
        ### PRESS_DICT ###
        self.DICT_PRESS_SN                          = "bxxxxxxxx"
        self.DICT_PRESS_STATUS_OPTIONS_n_COLORS     = [
                                                        ('Printing', 'lightgreen', '#ccffcc'),  # Light green
                                                        ('Printing with limitation', 'orange', '#ffe6cc'),  # Light orange
                                                        ('Proactive shutdown', '#999900', '#ffffcc'),  # Light yellow
                                                        ('Pending customer', 'purple', '#e6ccff'),  # Light purple
                                                        ('MD - Troubleshooting', 'red', '#ffcccc'),  # Light red
                                                        ('MD - Waiting for parts', 'red', '#ffcccc'),  # Light red
                                                        ('MD - Escalation', 'red', '#ffcccc')  # Light red
                                                    ]
        self.DICT_SHIFT_OPTIONS                     = ('Morning', 'Noon', 'Night')
        ### Dictionary ###
        self.DEFAULT_DICT                           = self.set_conf_dict()
        self.REF_META                               = {}
        self.META                                   = {}
        self.PRESS_DICT                             = {
                                                        "SN"                    : self.DICT_PRESS_SN,
                                                        "PRESS_STATUS_COLORS"   : self.DICT_PRESS_STATUS_OPTIONS_n_COLORS,
                                                        "DICT_SHIFT_OPTIONS"         : self.DICT_SHIFT_OPTIONS
                                                    }
        ### Inherent params ###
        self.lock = threading.Lock()                                                                                    # Add a lock attribute to the class
        self.conf_read_or_write_meta_data_json()
    def set_attribute(self, key, value):
        with self.lock:                                                                                                 # Use the lock when setting attributes
            self.META[key] = value
    def get_attribute(self, key):
        with self.lock:                                                                                                 # Use the lock when setting attributes
            return self.META.get(key, None)
    def set_conf_dict(self):
        tmp_dict = {"METADATA" : {}}
        for k, v in self.__dict__.items():
            tmp_dict["METADATA"][k] = v
        return tmp_dict
    def conf_read_or_write_meta_data_json(self):                                                                        # Function to write the default metadata
        path = self.METADATA_PATH
        def write_default_metadata():
            with open(path, 'w') as f:
                json.dump(self.DEFAULT_DICT, f, indent=4)
            return self.DEFAULT_DICT["METADATA"]
        if os.path.exists(path):                                                                                        # Check if the file exists
            with open(path, 'r') as file:
                meta_data = json.load(file)
            if meta_data["METADATA"]["METADATA_FLAG"]:                                                                  # Check the METADATA_FLAG
                result = meta_data["METADATA"]
            else:
                result = write_default_metadata()
        else:
            result = write_default_metadata()
        self.REF_META = copy.deepcopy(result)
        self.META = result
        return result

DMD = conf()
DMDD = DMD.META
def azure_initialization(applogger, shared_data):
    shared_data.MAINAGENT, shared_data.AZURECONNECT, shared_data.METADATA, shared_data.CONFIG = func_initial_azure(applogger=applogger, dmdd=DMDD)
    return shared_data.MAINAGENT, shared_data.AZURECONNECT, shared_data.METADATA, shared_data.CONFIG
