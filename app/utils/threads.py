import asyncio
import threading
import subprocess
import os
from datetime import datetime
from pyshark import LiveCapture
from .global_vars import raw_logs_path, parsed_logs_path


def sniff(
    interface: str,
    packets_per_file: int,
    file_event: threading.Event,
    stop_processing: threading.Event,
) -> None:
    counter = 0
    loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    while counter != 2:
        current_date: str = (
            f"{str(datetime.now()).split('.')[0].replace(' ', 'T').replace(':', '_')}Z"
        )
        file_path: str = os.path.join(raw_logs_path, f"pkt_{current_date}.pcap")
        with open(file_path, "w") as _:
            capture: LiveCapture = LiveCapture(
                interface=interface, output_file=file_path
            )
            capture.sniff(packet_count=packets_per_file)
            file_event.set()
            counter += 1
    stop_processing.set()


def process_file(file_event: threading.Event, stop_processing: threading.Event) -> None:
    while True:
        file_event.wait()
        file_event.clear()
        current_log_file = [file_name for file_name in os.listdir(raw_logs_path)][-1]
        output_file_path: str = os.path.join(
            parsed_logs_path,
            f"{current_log_file.split('.')[0]}.csv",
        )
        input_file_path: str = os.path.join(raw_logs_path, current_log_file)
        subprocess.run(
            f"echo 'input: {input_file_path}   output: {output_file_path}'", shell=True
        )
        # subprocess.run(f'cicflowmeter -f {current_log_file} -c {output_file_path}', shell=True)
        if stop_processing.is_set():
            break
