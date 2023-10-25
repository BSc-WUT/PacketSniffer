import threading
from utils.arg_parser import arg_parse
from utils.threads import sniff, process_file


def main() -> None:
    args = arg_parse()
    file_event = threading.Event()
    stop_processing = threading.Event()
    # sniff_thread = threading.Thread(target=sniff, args=(args.interface, args.packets_per_file, file_event))
    sniff_thread = threading.Thread(
        target=sniff, args=("Wi-Fi", 50, file_event, stop_processing)
    )
    process_file_thread = threading.Thread(
        target=process_file, args=(file_event, stop_processing)
    )

    sniff_thread.start()
    process_file_thread.start()
    sniff_thread.join()
    process_file_thread.join()


if __name__ == "__main__":
    main()
