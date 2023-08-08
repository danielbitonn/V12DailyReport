# TODO:
#  ################################################## Program Design ###################################################
#          REQUIREMENTS:
#                       IMPORTS
#          SYSTEM:
#                       GUI MANAGER
#                       APP LOGGER
#                       BKG # AZURE INTERFACE
#                       DATE & TIME PICKER [time-dimmed]
#

from src.scripts.system.config import DMDD
from src.scripts.system.applogger import APPLOGGER
from src.scripts.gui.gui_manager import main_gui_start

if __name__ == '__main__':
    # METADATA thread
    x=3
    print(f'fdsfsdf:{DMDD}')
    APPLOGGER.info(f'DONE # <read_or_write_meta_data_json()> has been completed <{x}>')

    # Main Gui Thread
    main_gui_start()
    # tr_main_gui_start = threading.Thread(target=main_gui_start(), daemon=True)
    # tr_main_gui_start.start()


    # Wait for the dtr_meta_data to be set
    # META_DATA = qtr_meta_data.get()
    # print(META_DATA)

    print("THE END")

