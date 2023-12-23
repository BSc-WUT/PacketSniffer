import threading
import os
from dotenv import load_dotenv
from pathlib import Path
from utils.arg_parser import arg_parse
from utils.threads import sniff, process_file, send_logs
from utils.global_vars import parsed_logs_path, raw_logs_path
from utils.logs import log


def main() -> None:
    args = arg_parse()
    file_event = threading.Event()
    stop_processing = threading.Event()
    send_logs_event = threading.Event()

    load_dotenv()
    interface: str = os.getenv('INTERFACE') if os.getenv('INTERFACE') else args.interface
    if not interface:
        raise ValueError('Interface is required for packet sniffing, please provide one in .env file with name INTERFACE or use command line argument `-i <interface>`')
    log(f"Sniffing on inteface: {interface}", "main")
    packets_per_file: int = int(os.getenv('PACKETS_PER_FILE')) if os.getenv('PACKETS_PER_FILE') else args.packets_per_file

    sniff_thread = threading.Thread(
        target=sniff,
        args=(interface, packets_per_file, file_event, stop_processing),
    )
    process_file_thread = threading.Thread(
        target=process_file, args=(file_event, stop_processing, send_logs_event)
    )
    send_logs_thread = threading.Thread(
        target=send_logs, args=(send_logs_event, stop_processing)
    )

    sniff_thread.start()
    process_file_thread.start()
    send_logs_thread.start()

    sniff_thread.join()
    process_file_thread.join()
    send_logs_thread.join()


if __name__ == "__main__":
    Path(parsed_logs_path).mkdir(parents=True, exist_ok=True)
    Path(raw_logs_path).mkdir(parents=True, exist_ok=True)
    main()