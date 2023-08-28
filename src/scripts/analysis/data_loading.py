import re
from datetime import datetime as dt
from src.scripts.gui.windows.win_utility import SHARE_DATA
def func_swap_day_month_in_date(date_string):
    if date_string:
        parts = date_string.split('-')
        if len(parts) == 3:
            parts[1], parts[2] = parts[2], parts[1]
            return '-'.join(parts)
    return date_string
def func_extract_date_from_filename(file_name):
    """Check if dates are exist in the name files"""
    match = re.search(r"\d{4}-\d{2}-\d{2}", file_name)
    if match:
        return func_swap_day_month_in_date(match.group())
    else:
        return None
def get_date_time_from_file(f):
    date_time_str = f.split('_To_')[1].rstrip('.csv')
    return dt.strptime(date_time_str, '%Y-%d-%m_%H-%M-%S')
def group_files_by_index(file_list):
    file_groups = {}
    file_dates = {f: get_date_time_from_file(f) for f in file_list}
    for f in file_list:
        components = f.split('___')
        index = components[2].split('_')[0]
        if index not in file_groups or file_dates[f] > file_dates[file_groups[index]]:
            file_groups[index] = f
    return list(file_groups.values())
def get_latest_files(list_of_files):
    pressDB_list = [f for f in list_of_files if f.endswith('.db') and 'PressDB' in f and 'COPY' not in f]
    indexes_list = group_files_by_index([f for f in list_of_files if f.endswith('.csv')])
    return indexes_list + pressDB_list
def data_loading():
    root_exported_files_path = SHARE_DATA.METADATA["FOLDERS_FULL_PATHS"]["FOLDERS_FULL_PATHS_EXPORTED"]
    EXPORTED_STORAGE = SHARE_DATA.EXPORTED_STORAGE
    SN = SHARE_DATA.PRESS
    DATE = SHARE_DATA.END_DATE
    downloaded_paths_data = {}
    relevant_files_from_azure = []
    relevant_files_from_local = []

    # TODO: Next version!
    TIME = SHARE_DATA.END_TIME
    START = SHARE_DATA.START_DATE
    START_TIME = SHARE_DATA.START_TIME
    try:
        print(EXPORTED_STORAGE[SN][DATE])
        the_relevant_files = [f_name for f_name in EXPORTED_STORAGE[SN][DATE]['files'] if DATE == func_extract_date_from_filename(f_name)]
        print(the_relevant_files)
        try:
            the_relevant_files = get_latest_files(list_of_files=the_relevant_files)
            print(the_relevant_files)
            return True
        except Exception as e:
            print("\033[91m{}\033[0m".format(e))
            return False
    except Exception as e:
        print("\033[91m{}\033[0m".format(e))
        return False

    # if SHARE_DATA.AZURE_CONNECT_FLAG:
    #     relevant_files_from_azure = [f_name for f_name in EXPORTED_STORAGE[SN] if DATE == func_extract_date_from_filename(f_name)]
    #     print(F"All files from {DATE} for {SN} are: {len(relevant_files_from_azure)}, {relevant_files_from_azure}")
    #     relevant_files_from_azure = get_latest_files(list_of_files=relevant_files_from_azure)
    #     print(F"Up to date files from {DATE}: {len(relevant_files_from_azure)}, {relevant_files_from_azure}")
    #     if len(relevant_files_from_azure) == 0:
    #         print(relevant_files_from_azure)
    #         print("##########: if-if")
    #         # TODO: Return because there's no files in Azure - Choose another date or any other strategy
    #     else:
    #         print("##########: if-if-else")
    #         # TODO: Read the relevant files
    #         # TODO: GOTO analysis phase
    # else:
    #     #TODO: READ LOCALLY
    #     if len(relevant_files_from_local) == 0:
    #         print(relevant_files_from_local)
    #         print("##########: else-if")
    #         # TODO: Return because there's no files in Azure - Choose another date or any other strategy
    #     else:
    #         print("##########: else-if-else")
    #         # TODO: Read the relevant files
    #         # TODO: GOTO analysis phase