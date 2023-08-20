import datetime
import json
import os
import subprocess
import sys
import time
import traceback

import pandas as pd

from src.scripts.system.applogger import APPLOGGER

INTEGRATION_MOO             = "INTEG"
PUSH_MOO                    = "PUSH"
PULL_MOO                    = "PULL"
MOOs                        = (PULL_MOO, PUSH_MOO, INTEGRATION_MOO)
DT_FORMAT                   = "%Y-%m-%d"
T_FORMAT                    = "%H:%M"
ARGS_INPUT_PRESS_SN_DEFAULT = 'bxxxxxxxx'
ARGS_INPUT_JSON_DEFAULT     = dict(press_sn=ARGS_INPUT_PRESS_SN_DEFAULT, mode=", ".join(MOOs), str_date=f"{datetime.datetime.now().strftime(f'{DT_FORMAT}')}", end_date=f"{datetime.datetime.now().strftime(f'{DT_FORMAT}')}", str_time="00:01", end_time=f"{datetime.datetime.now().strftime(f'{T_FORMAT}')}")
FATHER_PATH                 = 'sa_output'
ARGS_INPUT_JSON_FILE        = f'{FATHER_PATH}\\args_for_db_sa.json'
PAUSE01                     = 1
def recognize_data_type(data):
    if isinstance(data, dict):
        return "json"
    elif isinstance(data, list) and isinstance(data[0], dict):
        return "json"
    elif isinstance(data, pd.DataFrame):
        return "csv"
    elif isinstance(data, str) and data.startswith("http"):
        return "url"
    elif isinstance(data, str):
        return "txt"
    else:
        return "unknown"
def update_master_json(file_name, data):
    data_type = recognize_data_type(data=data)                                                                          # Recognize the type of the data
    master_file = os.path.join('output', 'data', 'jsons', 'MASTER_JSON.json')                                           # Define the name of the master JSON file - TODO: Move to SHAREDATA
    ### Serialize data based on its type ###
    if data_type == "csv":
        data = data.to_dict(orient='records')  # Convert DataFrame to list of dictionaries
    elif data_type == "unknown":
        data = str(data)                                                                                                # Convert unknown type to string
    try:                                                                                                                # Load the current contents of the master JSON file if exist
        with open(master_file, 'r') as file:
            master_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        master_data = {}
    master_data[file_name] = {"data_type": data_type, "data": data}                                                     # Update the data
    with open(master_file, 'w') as file:                                                                                # Save the updated data back
        json.dump(master_data, file, indent=4)
def load_master_json():
    """
    Loads the raw contents of the MASTER_JSON.json file.
    This function is suitable for operations that don't require understanding the data's original format, like checking
    if a particular filename exists in the master data.
    It doesn't process or convert any of the internal data structures.
    For example, if the file contains serialized CSV data (a list of dictionaries), that's how it will be returned.
    :return: A dictionary representing the raw contents of MASTER_JSON.json.
    """
    master_file = os.path.join('output', 'data', 'jsons', 'MASTER_JSON.json')  # Define the master JSON file
    with open(master_file, 'r') as file:
        raw_data = json.load(file)
    MASTER_JSON = {}
    for file_name, entry in raw_data.items():
        data_type = entry["data_type"]
        data = entry["data"]
        ### Deserialize data based on its type ###
        if data_type == "csv":
            data = pd.DataFrame(data)                                                                                   # Convert list of dictionaries to DataFrame
        MASTER_JSON[file_name] = {"data_type": data_type, "data": data}                                                 # For other types like 'json', 'txt', and 'url', data remains as-is
    return MASTER_JSON
def read_master_json():
    """
    Reads and processes the contents of the MASTER_JSON.json file.
    This function is designed for operations that require the data to be in its original format, converting serialized
    data back to its original Python format based on the 'data_type' attribute.
    For example, if an entry has a 'data_type' of "csv", the associated list of dictionaries will be converted back
    into a DataFrame before being returned.
    :return: A dictionary where each entry is in its original Python format.
    """
    master_file = os.path.join('output', 'data', 'jsons', 'MASTER_JSON.json')                                           # Define the master JSON file
    try:
        with open(master_file, 'r') as file:
            master_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}                                                                                                       # Return an empty dictionary if file not found or empty
    MASTER_JSON = {}
    for file_name, entry in master_data.items():
        data_type = entry["data_type"]
        data = entry["data"]
        ### Deserialize data based on its type ###
        if data_type == "csv":
            data = pd.DataFrame(data)                                                                                   # Convert list of dictionaries back to DataFrame
        elif data_type == "json":
            pass                                                                                                        # It's already a dictionary
        elif data_type in ["txt", "url"]:
            pass                                                                                                        # It's a string, no need for conversion
        elif data_type == "unknown":
            pass                                                                                                        # It's stored as a string
        MASTER_JSON[file_name] = {"data_type": data_type, "data": data}
    return MASTER_JSON
def logger_explain_template():
    return f'{sys.exc_info()[0]} >>> {sys.exc_info()[1]} >>> {traceback.extract_tb(list(sys.exc_info())[2])}'

def func_r_w_json(path, m, data=None):
    try:
        if m == 'r':
            with open(path, m) as rd:
                return json.load(rd)
        elif m == 'w':
            with open(path, m) as wr:
                json.dump(data, wr, indent=4)
        elif m == 'a':
            try:
                with open(path, 'r') as rd:
                    current_data = json.load(rd)
            except (FileNotFoundError, json.JSONDecodeError):
                current_data = {}
            current_data.update(data)
            with open(path, 'w') as wr:
                json.dump(current_data, wr, indent=4)
        else:
            APPLOGGER.debug(f'Debug: <func_r_w_json()> Invalid mode, please use "r" for read or "w" for write: <mode: {m}>, <path: {path}>, <data: {data}> >>> {logger_explain_template()}')
    except Exception as ex:
        APPLOGGER.error(f'Error: <func_r_w_json()> has been failed: <mode: {m}>, <path: {path}>, <data: {data}> >>> {ex} >>> {logger_explain_template()}')

def func_read_write_args_input_json_file(root_path=None):
    APPLOGGER.debug(f'Solution: Default dicionary {ARGS_INPUT_JSON_DEFAULT} has been written into editable JSON {ARGS_INPUT_JSON_FILE}')
    if root_path is None:
        root_path = ARGS_INPUT_JSON_FILE
    try:
        if not os.path.exists(FATHER_PATH):
            os.makedirs(FATHER_PATH)
        func_r_w_json(path=root_path, m='w', data=ARGS_INPUT_JSON_DEFAULT)
        try:
            subprocess.call(['notepad', root_path])
            time.sleep(PAUSE01)
            try:
                return func_r_w_json(path=root_path, m='r')
            except Exception as ex:
                APPLOGGER.error(f'Error: <func_read_write_json_file()> has been failed to Re-READ <{root_path}> >>> {ex} >>> {logger_explain_template()}')
        except Exception as ex:
            APPLOGGER.error(f'Error: <func_read_write_json_file()> has been failed to EDIT <{root_path}> >>> {ex} >>> {logger_explain_template()}')
    except Exception as ex:
        APPLOGGER.error(f'Error: <func_read_write_json_file()> has been failed to WRITE <{root_path}> >>> {ex} >>> {logger_explain_template()}')
def func_mandatory_requirements_inputs():
    pass
