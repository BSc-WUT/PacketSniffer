import psutil
import argparse


def arg_parse() -> list:
    possible_interfaces = psutil.net_if_addrs().keys()
    parser = argparse.ArgumentParser(
        prog="PacketSniffer",
        description="Sniffs Internet Packets from provided interface and saves it as csv file with CICFlowMeter parameters.",
    )
    parser.add_argument(
        "-i",
        "--interface",
        dest="interface",
        type=str,
        help=f"Choose one of possible interface values: {', '.join(possible_interfaces)}",
    )
    parser.add_argument(
        "-p",
        "--packets-per-file",
        dest="packets_per_file",
        type=int,
        help="Maximum number of packets per log file.",
    )
    args = parser.parse_args()
    return args
