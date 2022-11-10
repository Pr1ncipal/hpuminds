import argparse
import math
import time
import brainflow
import numpy as np
import serial

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds, BrainFlowError
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions, DetrendOperations
from brainflow.ml_model import MLModel, BrainFlowMetrics, BrainFlowClassifiers, BrainFlowModelParams
from brainflow.exit_codes import *

def main():
    BoardShim.enable_board_logger()
    DataFilter.enable_data_logger()
    MLModel.enable_ml_logger()

    BoardShim.enable_dev_board_logger()

    arduino = serial.Serial(port='COM4', baudrate=9600, timeout=.1)

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
    params.board_id = 0
    params.ip_port = 0
    params.serial_port = "COM5"
    params.mac_address = ""
    params.other_info = ""
    params.serial_number = ""
    params.ip_address = ""
    params.ip_protocol = 0
    params.timeout = 0
    params.file = ""
    params.streamer_params = ""

    board = BoardShim(params.board_id, params)
    master_board_id = board.get_board_id()
    sampling_rate = BoardShim.get_sampling_rate(master_board_id)
    board.prepare_session()
    board.start_stream(45000, params.streamer_params)

    while True:
        time.sleep(4)  # recommended window size for eeg metric calculation is at least 4 seconds, bigger is better
        data = board.get_board_data()
        # board.stop_stream()
        # board.release_session()

        eeg_channels = BoardShim.get_eeg_channels(int(master_board_id))
        bands = DataFilter.get_avg_band_powers(data, eeg_channels, sampling_rate, True)
        feature_vector = np.concatenate((bands[0], bands[1]))

        # calc concentration
        concentration_params = BrainFlowModelParams(BrainFlowMetrics.CONCENTRATION.value, BrainFlowClassifiers.KNN.value)
        concentration = MLModel(concentration_params)
        concentration.prepare()
        concen_perc = concentration.predict(feature_vector)
        print('Concentration: %f' % concen_perc)
        concentration.release()

        # calc relaxation
        # relaxation_params = BrainFlowModelParams(BrainFlowMetrics.RELAXATION.value,
        #                                          BrainFlowClassifiers.REGRESSION.value)
        # relaxation = MLModel(relaxation_params)
        #
        # relaxation.prepare()
        # relaxation_perc = relaxation.predict(feature_vector)
        # print('Relaxation: %f' % relaxation_perc)
        # relaxation.release()

        parsed_ouput = 1 + math.ceil(4 * concen_perc)
        arduino.write(bytes(f'{parsed_ouput}', 'utf-8'))

if __name__ == "__main__":
    main()