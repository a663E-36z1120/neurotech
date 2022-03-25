import time
from openbci_interface import Cyton

sample_rate = 250
port = '/dev/cu.usbserial-DM00CXN8'

with Cython(port) as board:
    board.set_board_mode('default')
    board.set_sample_rate(sample_rate)
    board.start_streaming()
    while True:
        sample = board.read_sample()
        time.sleep(0.95 / sample_rate)