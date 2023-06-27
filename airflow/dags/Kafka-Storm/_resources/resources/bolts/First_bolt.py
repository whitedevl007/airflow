from hdfs import InsecureClient  # Importing the necessary module
import json
from streamparse import Bolt
import time


class Emit(Bolt):  # Defining a class named Emit that extends the Bolt class

    def initialize(self, storm_conf, context):  # Initializing the bolt
        self.hdfs_client = InsecureClient('http://localhost:50070')  # Creating an HDFS client to connect to HDFS

    def process(self, tup):  # Method to process each tuple
        json_data = tup.values[0]  # Extracting the JSON data from the tuple
        try:
            user_data = json.loads(json_data)  # Parsing the JSON data
            personal_info = user_data.get('Personal_info')  # Extracting the 'Personal_info' field from the JSON data
            folder_name = personal_info['Name']  # Extracting the 'Name' field from the 'Personal_info' field
            folder_name = folder_name.replace(" ", "") + str(tup.id)  # Modifying the folder name with tuple id
            id = str(tup.id)  # Converting the tuple id to a string
            if json_data is not None:  # Checking if JSON data exists
                try:
                    self.write_to_hdfs(json_data, folder_name, id)  # Writing JSON data to HDFS
                    self.log(f'{folder_name} added to HDFS')  # Logging a success message
                except Exception as e:
                    self.log(f'HDFS Error: {e}')  # Logging an error message
                    # self.handle_hdfs_error(folder_name, json_data)  # Handling HDFS error
        except ValueError as v:
            self.log(f'ValueError: {v}')  # Logging an error message
            pass
        except TypeError as t:
            self.log(f'typeError: {t}')  # Logging an error message
            pass
        except KeyError as k:
            self.log(f'KeyError: {k}')  # Logging an error message
            pass
        except NameError as e:
            self.log(f'NameError: {e}')  # Logging an error message
            pass

    def write_to_hdfs(self, json_data, folder_name, id):  # Method to write data to HDFS
        while True:  # Retry loop for writing to HDFS
            try:
                with self.hdfs_client.write('/usercontextata/' + folder_name + f'/{id[-4:]}{str(folder_name.lower())}.json', encoding='utf-8', overwrite=True) as writer:  # Writing JSON data to HDFS file
                    writer.write(json_data)
                break  # Success, break the retry loop
            except Exception as e:
                self.log(f'HDFS Error: {e}')  # Logging an error message
                self.log('Retrying HDFS write...')  # Logging a retry message
                time.sleep(1)  # Wait for 1 second before retrying
