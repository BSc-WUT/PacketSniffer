from pyshark import LiveCapture
from datetime import datetime
import os
import argparse
import psutil
import threading
import subprocess
import asyncio


def sniff(interface: str, packets_per_file: int, file_event: threading.Event, stop_processing: threading.Event) -> None:
    counter = 0
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    while counter != 2:
        current_date: str = f"{str(datetime.now()).split('.')[0].replace(' ', 'T').replace(':', '_')}Z"
        file_path: str = os.path.join('logs', f"pkt_{current_date}.pcap")
        with open(file_path, 'w') as _:
            capture: LiveCapture = LiveCapture(interface=interface, output_file=file_path)
            capture.sniff(packet_count=packets_per_file)
            file_event.set()
            counter += 1
    stop_processing.set()


def process_file(logs_dir_name: str, file_event: threading.Event, stop_processing: threading.Event) -> None:
    while True:
        file_event.wait()
        file_event.clear()
        current_log_file = [file_name for file_name in os.listdir(logs_dir_name)][-1]
        subprocess.run(f"echo '{current_log_file}'", shell=True)
        if stop_processing.is_set():
            break


if __name__ == '__main__':
    possible_interfaces = psutil.net_if_addrs().keys()
    parser = argparse.ArgumentParser(
        prog='PacketSniffer',
        description='Sniffs Internet Packets from provided interface and saves it as csv file with CICFlowMeter parameters.'
    )
    parser.add_argument('-i', '--interface', dest="interface", type=str, help=f"Choose one of possible interface values: {', '.join(possible_interfaces)}")
    parser.add_argument('-p', '--packets-per-file', dest='packets_per_file', type=int, help='Maximum number of packets per log file.')
    args = parser.parse_args()

    file_event = threading.Event()
    stop_processing = threading.Event()
    #sniff_thread = threading.Thread(target=sniff, args=(args.interface, args.packets_per_file, file_event))
    sniff_thread = threading.Thread(target=sniff, args=("Wi-Fi", 50, file_event, stop_processing))
    process_file_thread = threading.Thread(target=process_file, args=('logs', file_event, stop_processing))

    sniff_thread.start()
    process_file_thread.start()

    sniff_thread.join()
    process_file_thread.join()

    
    

    