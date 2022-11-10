import argparse
import time
import numpy as np

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations


def main():
    BoardShim.enable_dev_board_logger()

    # parser = argparse.ArgumentParser()
    # # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
    # parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False,
    #                     default=0)
    # parser.add_argument('--ip-port', type=int, help='ip port', required=False, default=0)
    # parser.add_argument('--ip-protocol', type=int, help='ip protocol, check IpProtocolType enum', required=False,
    #                     default=0)
    # parser.add_argument('--ip-address', type=str, help='ip address', required=False, default='')
    # parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='')
    # parser.add_argument('--mac-address', type=str, help='mac address', required=False, default='')
    # parser.add_argument('--other-info', type=str, help='other info', required=False, default='')
    # parser.add_argument('--streamer-params', type=str, help='streamer params', required=False, default='')
    # parser.add_argument('--serial-number', type=str, help='serial number', required=False, default='')
    # parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
    #                     required=True)
    # parser.add_argument('--file', type=str, help='file', required=False, default='')
    # args = parser.parse_args()

    params = BrainFlowInputParams()
    board_id = 0
    params.ip_port = 0
    params.serial_port = "COM5"
    params.mac_address = ""
    params.other_info = ""
    params.serial_number = ""
    params.ip_address = ""
    params.ip_protocol = 0
    params.timeout = 0
    params.file = ""
    streamerparams = ""

    board = BoardShim(board_id, params)
    board.prepare_session()

    # board.start_stream () # use this for default options
    board.start_stream(45000, streamerparams)
    time.sleep(60)
    #data = board.get_current_board_data (256) # get latest 256 packages or less, doesnt remove them from internal buffer
    data = board.get_board_data()  # get all data and remove it from internal buffer
    board.stop_stream()
    board.release_session()

    # TODO: Maybe make it output to a JSON file
    file = open("log.txt", "w")
    for arr in data:
        str = "["
        for element in arr:
            str += f'{element}, '
        str += "]\n"
        file.write(f'{str}\n')
    file.close()

if __name__ == "__main__":
    main()
