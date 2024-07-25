import os
import time
import json
from collections import defaultdict
import logging
#basic config for logging, all log goes to app.log file
logging.basicConfig(
        filename="app.log",
        encoding="utf-8",
        filemode="a",
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
    )
def categorize_files_by_type(folder_path):

    if not os.path.exists(folder_path):
        logging.error('The directory does not exist')
        raise FileNotFoundError(f"The directory {folder_path} does not exist")

    if not os.path.isdir(folder_path):
        logging.error('The directory is not a directory')
        raise NotADirectoryError(f"{folder_path} is not a directory")

    result = defaultdict(list)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            extension = os.path.splitext(file)[1]
            size = str(round((os.path.getsize(file_path)/1024),1)) + " MB"
            last_m_time = time.ctime(os.path.getmtime(file_path))

            file_dict = {"name":file,"path":file_path,"size":size,"last modified time":last_m_time}
            logging_if_missing(file_path,extension,size)
            result[extension].append(file_dict)

    return dict(result)

#logging if one of expected statements is missing size and last mod. time cannot be none,so there is not any
def logging_if_missing(file_path,extension,file_dict):

    if file_path == "":
        logging.warning("File_path is missing")
    if extension == "":
        logging.warning("File extension is missing")
    if file_dict == "" or extension == "":
        logging.warning(file_dict)


result = categorize_files_by_type("TestTask")
print(json.dumps(result, indent=4))

