import os
import sys
import traceback
import pandas as pd
from io import StringIO
import json
from azure.storage.blob import BlobServiceClient

########################################################################################################################
########## Azure_System_Conf ###########################################################################################
# def logger_explain_template():
#     return f'{sys.exc_info()[0]} >>> {sys.exc_info()[1]} >>> {traceback.extract_tb(list(sys.exc_info())[2])}'
def func_check_and_process_readme(APPLOGGER, DMDD):
    if os.path.exists(DMDD["ROOT_README_FILE_NAME"]):
        with open(DMDD["ROOT_README_FILE_NAME"], 'r') as r_file:
            azure_str = r_file.read()
        if len(azure_str) < len(DMDD["AZK"]):
            azure_str = DMDD["AZK"]
            with open(DMDD["ROOT_README_FILE_NAME"], 'w') as w_file:
                w_file.write(azure_str)
    else:
        azure_str = DMDD["AZK"]
        with open(DMDD["ROOT_README_FILE_NAME"], 'w') as w_file:
            w_file.write(azure_str)
    APPLOGGER.info(azure_str)
    return azure_str
class AzureAgent:
    def __init__(self, connection_string=None, logger=None, DMDD=None):
        self.blob_service_client    = BlobServiceClient.from_connection_string(connection_string)
        self.storage_data           = {
                                        container.name : [blob.name for blob in self.blob_service_client.get_container_client(container.name).list_blobs()]
                                        for container in self.blob_service_client.list_containers()
                                        }
        self.list_of_containers     = [container.name for container in self.blob_service_client.list_containers()]
        self.logger = logger                                                                                            # Store the logger instance
        self.DMDD = DMDD
    def list_blobs(self, container_name):
        return [blob.name for blob in self.blob_service_client.get_container_client(container_name).list_blobs()]
    def get_blobs(self, container_name):
        return self.blob_service_client.get_container_client(container_name).list_blobs()
    def read_blob(self, blob_name, container_name):
        try:
            blob_client = self.blob_service_client.get_blob_client(container_name, blob_name)
            blob_bytes = blob_client.download_blob().readall()
            blob_string = blob_bytes.decode()  # Convert bytes to string
            file_type = blob_name.split('.')[-1]
            if file_type == 'csv':
                return pd.read_csv(StringIO(blob_string))
            elif file_type == 'json':
                return json.loads(blob_string)
            elif file_type == 'txt':
                return blob_string
            else:
                self.logger.debug(f"The file <{blob_name}> is unsupported file type: {file_type}")
                return None
        except Exception as e:
            self.logger.error(f"Error reading blob {blob_name}: {e}")
            return None
    def get_all_blobs_data(self, container_name):
        data = {}
        try:
            for b in self.list_blobs(container_name):
                data[b] = self.read_blob(blob_name=b, container_name=container_name)
        except Exception as e:
            self.logger.error(f"Error: <get_all_blobs> has been failed >>> {e} >>> {container_name} >>> >>> {self.logger_message_template()}")
        return data
    def get_confing(self):
        try:
            return self.get_all_blobs_data(container_name=self.DMDD["CONF_CONTAINER_NAME"])
        except Exception as e:
            self.logger.error(f"Error <get_confing> has been failed: >>> {e} >>> {self.logger_message_template()}")
            return {}
    def pull_blob(self, container_name, blob_name):
        try:
            data = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name).download_blob().readall()
            return data
        except Exception as ex:
            self.logger.error(f"Error <pull_blob> has been failed: during <{blob_name}>>>> {ex} >>> {self.logger_message_template()}")
            return None
    def push_blob(self, container_name, blob_name):
        try:                                                                                                            # TODO: uploading necessary files
            print("VSDVSSDVSDVSDVSDVSDVSDVSDSDVSDVSD")
        except Exception as ex:
            self.logger.error(f"Error <push_blob> has been failed: during <{blob_name}> to the container {container_name} >>> {ex} >>> {self.logger_message_template()}")
    def logger_message_template(self):
        return f'{sys.exc_info()[0]} >>> {sys.exc_info()[1]} >>> {traceback.extract_tb(list(sys.exc_info())[2])}'
def func_initial_azure(applogger, dmdd):
    azureConnect = ""
    metaData = {}
    mainAgent = AzureAgent(connection_string=f'{func_check_and_process_readme(APPLOGGER=applogger, DMDD=dmdd)}', logger=applogger, DMDD=dmdd)
    azureConnect = mainAgent.blob_service_client
    metaData = mainAgent.storage_data
    config = mainAgent.get_confing()
    return mainAgent, azureConnect, metaData, config
