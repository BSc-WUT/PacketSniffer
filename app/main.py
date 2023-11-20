import threading
from utils.arg_parser import arg_parse
from utils.threads import sniff, process_file, send_logs


def main() -> None:
    args = arg_parse()
    file_event = threading.Event()
    file_event.set()
    stop_processing = threading.Event()
    send_logs_event = threading.Event()

    sniff_thread = threading.Thread(
        target=sniff,
        args=(args.interface, args.packets_per_file, file_event, stop_processing),
    )
    process_file_thread = threading.Thread(
        target=process_file, args=(file_event, stop_processing, send_logs_event)
    )
    send_logs_thread = threading.Thread(
        target=send_logs, args=(send_logs_event, stop_processing)
    )

    #sniff_thread.start()
    process_file_thread.start()
    send_logs_thread.start()

    #sniff_thread.join()
    process_file_thread.join()
    send_logs_thread.join()


if __name__ == "__main__":
    main()
