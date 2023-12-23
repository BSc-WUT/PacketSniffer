import asyncio
import threading
import subprocess
import os
from dotenv import load_dotenv
from datetime import datetime
from pyshark import LiveCapture
from .global_vars import raw_logs_path, parsed_logs_path
from .api_calls import get_active_model_name, predict_flow, save_flow_to_db
from .helpers import load_flows
from .logs import log


def sniff(
    interface: str,
    packets_per_file: int,
    file_event: threading.Event,
    stop_processing: threading.Event,
) -> None:
    loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    while True:
        current_date: str = (
            f"{str(datetime.now()).split('.')[0].replace(' ', 'T').replace(':', '_')}Z"
        )
        file_path: str = os.path.join(raw_logs_path, f"pkt_{current_date}.pcap")
        log(f"Sniffing packets, created packets log file: {file_path}", "utils.threads.sniff")
        with open(file_path, "w") as _:
            capture: LiveCapture = LiveCapture(
                interface=interface, output_file=file_path
            )
            capture.sniff(packet_count=packets_per_file if packets_per_file else 100)
        file_event.set()
    
    stop_processing.set()


def process_file(file_event: threading.Event, stop_processing: threading.Event, send_logs: threading.Event) -> None:
    while True:
        file_event.wait()
        file_event.clear()
        current_logs_file = [file_name for file_name in os.listdir(raw_logs_path)]
        if current_logs_file:
            current_log_file: str = max([os.path.join(raw_logs_path, file_path) for file_path in current_logs_file], key=os.path.getctime)
            output_file_path: str = os.path.join(parsed_logs_path, f"{os.path.split(current_log_file)[1].split('.')[0]}.csv")
            log(f"Creating csv file: {output_file_path} from logs with cicflowmeter", "utils.threads.process_file")
            subprocess.run(
                f"cicflowmeter -f {current_log_file} -c {output_file_path}", shell=True
            )
            log("Created csv file with cicflowmeter", "utils.threads.process_file")
            if stop_processing.is_set():
                break
            send_logs.set()


def send_logs(send_logs_event: threading.Event, stop_processing: threading.Event) -> None:
    load_dotenv()
    ml_api_url: str = f"{os.getenv('ML_API')}:{os.getenv('ML_API_PORT')}"
    db_api_url: str = f"{os.getenv('DB_API')}:{os.getenv('DB_API_PORT')}"
    active_model_name: str = get_active_model_name(ml_api_url)
    flows = load_flows()
    if not active_model_name:
        raise ValueError('No active model')
    while True:
        send_logs_event.wait()
        send_logs_event.clear()
        for flow in flows:
            flow['label'] = predict_flow(ml_api_url, active_model_name, flow)
            log(f"Predicted flow with label: {flow.get('label')}", "utils.threads.send_logs") 

            save_flow_to_db(db_api_url, flow)
            log(f"Saved predicted flow in database", "utils.threads.send_logs")

        if stop_processing.is_set():
            break