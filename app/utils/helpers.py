import os
import csv
from .global_vars import parsed_logs_path

def load_flows() -> dict:
    logs_file_paths: list = os.listdir(parsed_logs_path)
    with open(os.path.join(parsed_logs_path, logs_file_paths[0]), 'r') as file_handler:
        logs_reader = csv.reader(file_handler)
        columns: list = next(logs_reader)
        for log in logs_reader:
            flow = {column: value for column, value in zip(columns, log)}
            yield flow