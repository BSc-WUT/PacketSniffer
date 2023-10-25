import os


### DIR NAMES
ROOT_DIR_NAME = "app"
PARSED_LOGS_DIR_NAME = "parsed"
RAW_LOGS_DIR_NAME = "raw"
LOGS_DIR_NAME = "logs"


### PATHS
logs_path = os.path.join(ROOT_DIR_NAME, LOGS_DIR_NAME)
parsed_logs_path = os.path.join(logs_path, PARSED_LOGS_DIR_NAME)
raw_logs_path = os.path.join(logs_path, RAW_LOGS_DIR_NAME)
