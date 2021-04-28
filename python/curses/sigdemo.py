import signal
import sys

def signal_handler(sig, frame):
    print('signal_handler')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.pause()
