from src.scripts.cloud.azure_interface import func_initial_azure
from datetime import datetime as dt, timedelta as td
import threading
import os
import glob
import json
import getpass
import socket
import copy
def func_remove_symbols(input_string):
    return ''.join(char.lower() for char in input_string if char.isalnum())
def folders_handler(path):
    if not os.path.exists(path):
        os.makedirs(path)
def old_logs_deletion_files_automation():
    cutoff = dt.now() - td(days=DMDD["LOCAL_METADATA"]["LOG_DAYS_TO_DELETE"])
    log_files = glob.glob(f'{DMDD["LOCAL_METADATA"]["LOG_PATH_FULL"]}\\{DMDD["LOCAL_METADATA"]["LOG_PREFIX"]}*')
    for log_file in log_files:
        date_str = log_file.split('__')[2]                                                                              # Extract date from filename
        file_date = dt.strptime(date_str, DMDD["LOCAL_METADATA"]['DT_FORMAT'])
        if file_date < cutoff:                                                                                          # If file is older than X days, delete it
            os.remove(log_file)
            DMDD["LOCAL_METADATA"]["DELETED_FILES"].append(log_file)
    return DMDD["LOCAL_METADATA"]["DELETED_FILES"]
class conf:
    def __init__(self):
        self.initializing_metadata_dictionaries()
        ################################################################################################################
        self.AZURE_METADATA                         = {}
        self.PRESS_DICT                             = {
                                                        "SN"                    : self.PREVIOUS_PRESS_SN,
                                                        "PRESS_STATUS_COLORS"   : self.DICT_PRESS_STATUS_OPTIONS_n_COLORS,
                                                        "DICT_SHIFT_OPTIONS"    : self.DICT_SHIFT_OPTIONS
                                                      }
        self.conf_read_or_write_meta_data_json()
        ####################################### Inherent params ########################################################
        self.lock = threading.Lock()                                                                                    # Add a lock attribute to the class
        ################################################################################################################
        ################################################################################################################
        ################################################################################################################
    def initializing_metadata_dictionaries(self):
        self.flags()
        self.vers()
        self.files()
        self.formats()
        self.folders()
        self.paths_f()
        self.logs()
        self.azure()
        self.user()
        self.gui()
        self.esexporter()
        self.daily_report()
        ############################################# Create LOCAL_RAW_DATA ############################################
        self.LOCAL_RAW_DATA = self.set_sys_dictionary()
        self.LOCAL_METADATA = copy.deepcopy(self.LOCAL_RAW_DATA["LOCAL_METADATA"])
        ################################################################################################################
    def flags(self):
        ################################################################################################################
        ################################################## FLAGS  ######################################################
        self.LOCAL_METADATA_FLAG = 0
        self.ANIMATION_OR_PICTURE_FLAG = 1  # Animations or pictures for "Loaders"
        self.CHECK_QUEUE_FREQ = 100
    def vers(self):
        self.AZURE_METADATA_VER = "v001"
        self.VERSION = "v117"
        self.METADATA_DATE = "2023-08-22"
        self.PREV_VERSION = "v116"
        self.DFE_VERSION = "8.2.0.137.0"
        self.DFE_VERSION_DATE = "2023-03-01"
        self.PLC_VERSION = "V1.4.58.7"
        self.PLC_VERSION_DATE = "2023-03-01"
        self.SW_VERSION = "16000.0.973- patch.71"
        self.SW_VERSION_DATE = "2023-03-01"
        self.json_ver = "1.1.1"
        self.app_ver = "1.1.1"
        self.daily_report_ver = "v109"
    def files(self):
        self.METADATA_FILE_NAME     = "sys_db.json"
        self.METADATA_PATH          = f"./src/metadata/{self.METADATA_FILE_NAME}"
    def formats(self):
        self.DT_FORMAT                              = "%Y-%m-%d"
        self.T_FORMAT                               = "%H:%M"
        self.DT_YYYY_MM_DD__HH_MM                   = f"{self.DT_FORMAT }__{self.T_FORMAT}"
        self.METADATA_TODAY                         = dt.now().strftime(f'{self.DT_FORMAT}')
    def folders(self):
        self.ROOT_OUTPUT_PATH                       = "output"
        self.FILES_FOLDER_PATH                      = "files"
        self.IMAGES_PATH                            = "images"
        self.DATA_PATH                              = "data"
        self.LOG_PATH                               = "log"
        self.FILES_PATH_FULL                        = os.path.join(self.ROOT_OUTPUT_PATH, self.FILES_FOLDER_PATH)
        self.IMAGES_PATH_FULL                       = os.path.join(self.ROOT_OUTPUT_PATH, self.IMAGES_PATH)
        self.DATA_PATH_FULL                         = os.path.join(self.ROOT_OUTPUT_PATH, self.DATA_PATH)
        self.LOG_PATH_FULL                          = os.path.join(self.ROOT_OUTPUT_PATH, self.LOG_PATH)
        self.folders_arch                           = {
                                                        "fa_PushExpDataPathRel"	    : "push_exported_data\\",
                                                        "fa_PushExpDataPathRelCMD"	: "push_exported_data_CMD\\",
                                                        "fa_PullExpDataPathRel"		: "pull_data\\"
                                                        }
        self.folders_arch_comb                      = {
                                                        "fa_Images_comb"		    :"Images",
                                                        "fa_comb_logs"			    :"output\\logs",
                                                        "fa_comb_output_images"		:"output\\images",
                                                        "fa_comb_output_files"		:"output\\files",
                                                        "fa_comb_push"				:"data\\push_exported_data",
                                                        "fa_comb_pull"				:"data\\pull_imported_data"
                                                        }
        self.folders_to_upload                      = {
                                                        "fa_comb_push"				:["data\\push_exported_data",		 1,	1],
                                                        "fa_comb_logs"				:["output\\logs",					 1,	0],
                                                        "fa_comb_output_images"		:["output\\images",					 0,	0],
                                                        "fa_comb_output_files"		:["output\\files",					 0,	0]
                                                        }
        self.sa_folders_to_upload                   = {
                                                        "sa_fa_comb_logs"			:"sa_output\\logs",
                                                        "sa_fa_comb_output_images"	:"sa_output\\images",
                                                        "sa_fa_comb_output_files"	:"sa_output\\files",
                                                        "sa_fa_comb_data_pull"		:"sa_output\\data\\pull_imported_data",
                                                        "sa_fa_comb_data_push"		:"sa_output\\data\\push_imported_data"
                                                        }
    def paths_f(self):
        self.paths                                  = {
                                                        "PressEsExporter"           : "S:\\Press\\PressTools.EsExporter.exe",
                                                        "exportedData"              : "C:\\ExportedEsData\\",
                                                        "exBatPath"                 : "bats\\",
                                                        "exDataPath"                : "data\\",
                                                        "PushExpDataPathRel"        : "data\\push_exported_data\\",
                                                        "PushExpDataPathRelCMD"     : "data\\push_exported_data_CMD",
                                                        "PullExpDataPathRel"        : "data\\pull_data\\",
                                                        "sqldbPath"                 : "sqldb\\",
                                                        "databaseName"              : "PressDB.db",
                                                        "sqldbPath_csv"             : "sqldb\\db_csv",
                                                        "pressDBpath"               : "S:\\Press\\PressDB.db",
                                                        "exe_comm"                  : "bats\\V12Daily_report_v109.exe",
                                                        "analysis_data_root_path"   : "data\\pull_data"
                                                        }
        self.batsFiles                              = {"press-bat-exporter"         : "bats\\GCSGetRecorded.bat"}
        self.freecmd                                = {"comm"                       : "@echo off && echo V12 && pause"}
    def logs(self):
        self.LOG_DAYS_TO_DELETE                     = 1
        self.LOG_FATAL_ERRORS                       = []
        self.DELETED_FILES                          = []
        self.LOG_PREFIX                             = "log__"
        self.LOG_T_FORMAT                           = "%H-%M"
        self.LOG_YYYY_MM_DD__HH_MM                  = f"{self.DT_FORMAT }__{self.LOG_T_FORMAT}"
        self.logApp                                 = {"AppLogName": "AppLogger", "fields": ["asctime", "levelname", "message", "name"]}
    def azure(self):
        self.ROOT_README_FILE_NAME                  = "README.txt"
        self.AZK                                    = "DefaultEndpointsProtocol=https;AccountName=v12daily;AccountKey=2tBxBHZwM5WNyzPAyozRtsircGCFBAMN2S3TfZGFN923bIlkWAjdn5scM5vV5TkYPFKvukfD/cL5+AStMluGag==;EndpointSuffix=core.windows.net"
        self.LOCAL_MACHINE                          = func_remove_symbols(socket.gethostname())
        self.USER                                   = getpass.getuser()
        self.CONF_CONTAINER_NAME                    = "sysdb"
        self.container_name                         = "gcsteamcont"
        self.prssSNSeparator                        = "___SN___"
        self.combineSeperator                       = "_COMB"
        self.dfSeparator                            = "_From"
        self.output_json_path                       = "data\\"
        self.output_json_name                       = "storage_containers_blobs.json"
    def user(self):
        self.users_pc                               = {"hpcnd1270882": "biton"}
        self.presses                                = {
                                                        "b70001001": "70001001",
                                                        "b70001002": "70001002",
                                                        "b70001003": "70001003",
                                                        "b70001004": "70001004",
                                                        "b70001005": "70001005"
                                                    }
        self.PREVIOUS_PRESS_SN                          = "bxxxxxxxx"
    def gui(self):
        self.widget_sizes                           = {"width": 30, "height": 5}
        self.color_name_mapping                     = {
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
    def esexporter(self):
        self.indexes                                = {
                                                        "press-state-history": "press-state-history*",
                                                        "restart-history": "restart-history*",
                                                        "event-history": "*event-history*"
                                                    }
    def daily_report(self):
        self.DICT_PRESS_STATUS_OPTIONS_n_COLORS     = [
                                                        ('Printing',                    'lightgreen',      '#ccffcc'),      # Light green
                                                        ('Printing with limitation',    'orange',          '#ffe6cc'),      # Light orange
                                                        ('Proactive shutdown',          '#999900',         '#ffffcc'),      # Light yellow
                                                        ('Pending customer',            'purple',          '#e6ccff'),      # Light purple
                                                        ('MD - Troubleshooting',        'red',             '#ffcccc'),      # Light red
                                                        ('MD - Waiting for parts',      'red',             '#ffcccc'),      # Light red
                                                        ('MD - Escalation',             'red',             '#ffcccc')       # Light red
                                                    ]
        self.DICT_SHIFT_OPTIONS                     = ('Morning', 'Noon', 'Night')
        self.shift_options                          = {
                                                        "Morning": 1,
                                                        "Noon": 0,
                                                        "Night": 0
                                                    }
        self.topics_menu                            = {
                                                        "--Troubleshooting--":  [
                                                                                {
                                                                                  "topic": "SW issue",
                                                                                  "description": "Description for SW issue",
                                                                                  "family": "Other",
                                                                                  "family_colormap": "spring"
                                                                                },
                                                                                {
                                                                                  "topic": "PQ issue",
                                                                                  "description": "Description for PQ issue",
                                                                                  "family": "PQ issue",
                                                                                  "family_colormap": "Purples"
                                                                                },
                                                                                {
                                                                                  "topic": "PQ issue + fix / clean",
                                                                                  "description": "Description for PQ issue requiring fix or cleaning",
                                                                                  "family": "PQ issue",
                                                                                  "family_colormap": "Purples"
                                                                                },
                                                                                {
                                                                                  "topic": "PQ issue + Part replace",
                                                                                  "description": "Description for PQ issue requiring part replacement",
                                                                                  "family": "PQ issue",
                                                                                  "family_colormap": "Purples"
                                                                                },
                                                                                {
                                                                                  "topic": "PQ issue + Consumable replace",
                                                                                  "description": "PQ issue requiring consumable replacement",
                                                                                  "family": "PQ issue",
                                                                                  "family_colormap": "Purples"
                                                                                },
                                                                                {
                                                                                  "topic": "HW issue",
                                                                                  "description": "Description for HW issue",
                                                                                  "family": "HW issue",
                                                                                  "family_colormap": "Reds"
                                                                                },
                                                                                {
                                                                                  "topic": "HW issue + fix / clean",
                                                                                  "description": "Description for HW issue requiring fix or cleaning",
                                                                                  "family": "HW issue",
                                                                                  "family_colormap": "Reds"
                                                                                },
                                                                                {
                                                                                  "topic": "HW issue + Part replace",
                                                                                  "description": "Description for HW issue requiring part replacement",
                                                                                  "family": "HW issue",
                                                                                  "family_colormap": "Reds"
                                                                                },
                                                                                {
                                                                                  "topic": "HW issue + Consumable replace",
                                                                                  "description": "HW issue requiring consumable replacement",
                                                                                  "family": "HW issue",
                                                                                  "family_colormap": "Reds"
                                                                                },
                                                                                {
                                                                                  "topic": "other",
                                                                                  "description": "Description for other site reasons",
                                                                                  "family": "Other",
                                                                                  "family_colormap": "spring"
                                                                                }
                                                                              ],
                                                        "--Active actions--":   [
                                                                                {
                                                                                  "topic": "Power up",
                                                                                  "description": "Description or notes for Power up",
                                                                                  "family": "Other",
                                                                                  "family_colormap": "spring"
                                                                                },
                                                                                {
                                                                                  "topic": "Part replacement",
                                                                                  "description": "Description for Part replacement",
                                                                                  "family": "HW issue",
                                                                                  "family_colormap": "Reds"
                                                                                },
                                                                                {
                                                                                  "topic": "Scheduled Maintenance",
                                                                                  "description": "Description for Scheduled Maintenance",
                                                                                  "family": "Maintenance",
                                                                                  "family_colormap": "Greens"
                                                                                },
                                                                                {
                                                                                  "topic": "Unscheduled Maintenance",
                                                                                  "description": "Description for Unscheduled Maintenance",
                                                                                  "family": "Maintenance",
                                                                                  "family_colormap": "Greens"
                                                                                },
                                                                                {
                                                                                  "topic": "Web break",
                                                                                  "description": "Description for Unscheduled Maintenance",
                                                                                  "family": "HW issue",
                                                                                  "family_colormap": "Reds"
                                                                                },
                                                                                {
                                                                                  "topic": "other",
                                                                                  "description": "Description for other site reasons",
                                                                                  "family": "Other",
                                                                                  "family_colormap": "spring"
                                                                                }
                                                                              ],
                                                        "--Site's reasons--":   [
                                                                            {
                                                                              "topic": "Operator duties",
                                                                              "description": "Description for Operator duties",
                                                                              "family": "Other",
                                                                              "family_colormap": "spring"
                                                                            },
                                                                            {
                                                                              "topic": "Pending job",
                                                                              "description": "Description for Pending job",
                                                                              "family": "Other",
                                                                              "family_colormap": "spring"
                                                                            },
                                                                            {
                                                                              "topic": "Pending substrate",
                                                                              "description": "Description for Pending substrate",
                                                                              "family": "Other",
                                                                              "family_colormap": "spring"
                                                                            },
                                                                            {
                                                                              "topic": "Site maintenance",
                                                                              "description": "Description for Site maintenance",
                                                                              "family": "Maintenance",
                                                                              "family_colormap": "Greens"
                                                                            },
                                                                            {
                                                                              "topic": "other",
                                                                              "description": "Description for other site reasons",
                                                                              "family": "Other",
                                                                              "family_colormap": "spring"
                                                                            },
                                                                            {
                                                                              "topic": "Select",
                                                                              "description": "",
                                                                              "family": "Other",
                                                                              "family_colormap": "spring"
                                                                            }
                                                                          ]
                                                    }
        self.state_colors                           = {
                                                        "Power-Up"                  : "#87CEFA",
                                                        "Init"                      : "#9370DB",
                                                        "Off"                       : "#BC0E00",
                                                        "Service"                   : "#EBB517",
                                                        "Standby"                   : "#FFD700",
                                                        "GetReady"                  : "#90EE90",
                                                        "Ready"                     : "#008000",
                                                        "Print"                     : "#0000FF",
                                                        "Pre / Post Print"          : "#20B2AA",
                                                        "Shutdown"                  : "#778899",
                                                        "Restart"                   : "#FF8C00"
                                                    }
        self.press_status_colors                    = {
                                                        "Printing"                  : "#ccffcc",
                                                        "Printing with limitation"  : "#ffe6cc",
                                                        "Proactive shutdown"        : "#ffffcc",
                                                        "Pending customer"          : "#e6ccff",
                                                        "MD - Troubleshooting"      : "#ffcccc",
                                                        "MD - Waiting for parts"    : "#ffcccc",
                                                        "MD - Escalation"           : "#ffcccc"
                                                    }
    def set_sys_dictionary(self):
        tmp_dict = {"LOCAL_METADATA": {}}
        for k, v in self.__dict__.items():
            tmp_dict["LOCAL_METADATA"][k] = v
        return tmp_dict
    def set_attribute(self, key, value):
        with self.lock:                                                                                                 # Use the lock when setting attributes
            self.METADATA[key] = value
    def get_attribute(self, key):
        with self.lock:                                                                                                 # Use the lock when setting attributes
            return self.METADATA.get(key, None)
    def conf_read_or_write_meta_data_json(self):                                                                        # Function to write the default metadata
        path = self.METADATA_PATH
        def write_default_metadata():
            with open(path, 'w') as f:
                json.dump(self.LOCAL_RAW_DATA, f, indent=2)
            return self.LOCAL_RAW_DATA
        if os.path.exists(path):                                                                                        # Check if the file exists
            try:
                with open(path, 'r') as file:
                    meta_data = json.load(file)
                if meta_data["LOCAL_METADATA"]["LOCAL_METADATA_FLAG"]:                                                  # Check the METADATA_FLAG
                    result = meta_data
                else:
                    result = write_default_metadata()
            except:
                result = write_default_metadata()
        else:
            result = write_default_metadata()

        self.LOCAL_RAW_DATA         = copy.deepcopy(result)
        self.LOCAL_METADATA         = copy.deepcopy(result["LOCAL_METADATA"])
        # self.METADATA = result
        return result
DMD = conf()
DMDD = DMD.LOCAL_RAW_DATA
def azure_initialization(applogger, shared_data):
    shared_data.AZURE_MAINAGENT, shared_data.AZURE_STORAGE, shared_data.AZURE_METADATA, shared_data.AZURE_CONNECT_FLAG = func_initial_azure(applogger=applogger, local_metadata=DMD.LOCAL_METADATA)
    if shared_data.AZURE_CONNECT_FLAG:
        shared_data.REF_AZURE_METADATA = copy.deepcopy(shared_data.AZURE_METADATA)
        shared_data.METADATA = copy.deepcopy(shared_data.AZURE_METADATA["AZURE_METADATA"])
        try:
            with open(DMD.LOCAL_METADATA["METADATA_PATH"], 'r') as f:
                _data = json.loaf(f)
        except:
            _data = copy.deepcopy(DMD.LOCAL_RAW_DATA)
        _data.update(shared_data.AZURE_METADATA)
        with open(DMD.LOCAL_METADATA["METADATA_PATH"], 'w') as f:
            json.dump(_data, f, indent=2)
    else:
        shared_data.METADATA = copy.deepcopy(DMD.LOCAL_METADATA)
    return
