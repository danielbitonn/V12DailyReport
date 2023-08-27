# TODO:
#       AZURE_PUSH: uploading necessary files - SAVING LOCALLY - BASED ON COMMON PATH                                    NEXT
#       README.txt location needs to move!                                                                              SOMEDAY
########################################################################################################################
import os
import sys
import traceback
import pandas as pd
from io import StringIO
import json
from azure.storage.blob import BlobServiceClient
########################################################################################################################
########## Azure_System_Conf ###########################################################################################
def logger_message_template():
    return f'{sys.exc_info()[0]} >>> {sys.exc_info()[1]} >>> {traceback.extract_tb(list(sys.exc_info())[2])}'
def func_check_and_process_readme(APPLOGGER, LOCAL_METADATA):                                                           # TODO: MOVE LOCATION!!!!
    if os.path.exists(LOCAL_METADATA["ROOT_README_FILE_NAME"]):
        with open(LOCAL_METADATA["ROOT_README_FILE_NAME"], 'r') as r_file:
            azure_str = r_file.read()
        if len(azure_str) < len(LOCAL_METADATA["AZK"]):
            azure_str = LOCAL_METADATA["AZK"]
            with open(LOCAL_METADATA["ROOT_README_FILE_NAME"], 'w') as w_file:
                w_file.write(azure_str)
    else:
        azure_str = LOCAL_METADATA["AZK"]
        with open(LOCAL_METADATA["ROOT_README_FILE_NAME"], 'w') as w_file:
            w_file.write(azure_str)
    APPLOGGER.info(azure_str)
    return azure_str
class AzureAgent:
    def __init__(self, connection_string=None, logger=None, LOCAL_METADATA=None):
        self.AZURE_CONNECTION_FLAG = False
        self.logger = logger                                                                                            # Store the logger instance
        self.LOCAL_METADATA = LOCAL_METADATA
        self.AZURE_METADATA = {}
        self.AZURE_STORAGE = {}
        try:
            self.blob_service_client    = BlobServiceClient.from_connection_string(connection_string)
            self.list_of_containers     = [container.name for container in self.blob_service_client.list_containers()]
            self.AZURE_CONNECTION_FLAG = True
            if self.logger:
                self.logger.info("Successfully connected to Azure Storage.")
        except Exception as ex:
            if self.logger:
                self.logger.error(f"Failed to connect to Azure Storage. Error: {ex}")
    def azure_storage_map(self):
        self.AZURE_STORAGE = {
                                container.name: [blob.name for blob in self.blob_service_client.get_container_client(container.name).list_blobs()]
                                for container in self.blob_service_client.list_containers()
                                }
        return self.AZURE_STORAGE
    def list_blobs(self, container_name):
        return [blob.name for blob in self.blob_service_client.get_container_client(container_name).list_blobs()]
    def read_blob(self, container_name, blob_name):
        try:
            blob_client = self.blob_service_client.get_blob_client(container_name, blob_name)
            blob_bytes = blob_client.download_blob().readall()
            blob_data = blob_bytes.decode()                                                                             # Convert bytes to string
            file_type = blob_name.split('.')[-1]
            if file_type == 'csv':
                return pd.read_csv(StringIO(blob_data))
            elif file_type == 'json':
                return json.loads(blob_data)
            elif file_type == 'txt':
                return blob_data
            else:
                self.logger.debug(f"The file <{blob_name}> is unsupported file type: {file_type}")
                return blob_data
        except Exception as e:
            self.logger.error(f"Error reading blob {blob_name}: {e}")
            return None
    def get_all_blobs_data(self, container_name):
        data = {}
        try:
            for b in self.list_blobs(container_name):
                data[b] = self.read_blob(container_name=container_name, blob_name=b)
        except Exception as e:
            self.logger.error(f"Error: <get_all_blobs> has been failed >>> {e} >>> {container_name} >>> >>> {logger_message_template()}")
        return data
    def get_azure_metadata(self):
        try:
            self.AZURE_METADATA = self.get_all_blobs_data(container_name=self.LOCAL_METADATA["CONF_CONTAINER_NAME"])
            return self.AZURE_METADATA[self.LOCAL_METADATA["METADATA_FILE_NAME"]]
        except Exception as e:
            self.logger.error(f"Error <get_azure_metadata> has been failed: >>> {e} >>> {logger_message_template()}")
            return {}
    def push_blob(self, container_name, blob_name):
        try:
            # TODO: uploading necessary files - SAVING LOCALY - BASED ON COMMON PATH                                    NEXT
            print("VSDVSSDVSDVSDVSDVSDVSDVSDSDVSDVSD")
        except Exception as ex:
            self.logger.error(f"Error <push_blob> has been failed: during <{blob_name}> to the container {container_name} >>> {ex} >>> {logger_message_template()}")
def func_initial_azure(applogger, local_metadata):
    _temp_azure_storage_map = {}
    _temp_azure_metadata = {}
    mainAgent = AzureAgent(connection_string=f'{func_check_and_process_readme(APPLOGGER=applogger, LOCAL_METADATA=local_metadata)}', logger=applogger, LOCAL_METADATA=local_metadata)
    if mainAgent.AZURE_CONNECTION_FLAG:
        _temp_azure_storage_map = mainAgent.azure_storage_map()
        _temp_azure_metadata    = mainAgent.get_azure_metadata()
    return mainAgent, _temp_azure_storage_map, _temp_azure_metadata, mainAgent.AZURE_CONNECTION_FLAG
