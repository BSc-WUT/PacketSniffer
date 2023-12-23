import os
import csv
from .global_vars import parsed_logs_path
from .logs import log

def load_flows() -> dict:
    logs_file_paths: list = os.listdir(parsed_logs_path)
    latest_log_file_path: str = max([os.path.join(parsed_logs_path, file_path) for file_path in logs_file_paths], key=os.path.getctime)
    log(f"Latest file name: {latest_log_file_path}")
    with open(latest_log_file_path, 'r') as file_handler:
        logs_reader = csv.reader(file_handler)
        try:
            columns: list = next(logs_reader)
            for log in logs_reader:
                flow = {column: value for column, value in zip(columns, log)}
                yield flow
        except StopIteration:
            log(f"File: {latest_log_file_path} is empty")