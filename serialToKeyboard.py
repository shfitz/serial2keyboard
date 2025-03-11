import serial
import time
from pynput.keyboard import Key, Controller
import sys
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class ArduinoController:
    def __init__(self, port, baud_rate=9600):
        self.keyboard = Controller()
        self.port = port
        self.baud_rate = baud_rate
        self.key_mappings = {
            'A': 'A',
            'D': 'D',
            'W': 'W',
            ' ': ' '
        }
        self.ser = None

    def connect(self):
        '''Attempting to connect to Arduino'''
        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=1)
            time.sleep(2)
            logger.info(f'Connected to Arduino on {self.port}')
            return True
        except serial.SerialException as e:
            logger.error(f'Failed to connect to Arduino: {e}')
            return False

    def handle_button_event(self, button, state):
        if button in self.key_mappings:
            key = self.key_mappings[button]
            if state == '0':
                logger.info(f'Pressing {button} (Key: {key})')
                self.keyboard.press(key)
            elif state == '1':
                logger.info(f'Releasing {button} (Key: {key})')
                self.keyboard.release(key)

    def run(self):
        if not self.connect():
            return

        logger.info('Waiting for Arduino start signal...')
      

        logger.info('Starting main loop')
        while True:
            try:
                if self.ser.in_waiting:
                    line = self.ser.readline().decode('utf-8').strip()
                    if ':' in line:
                        button, state = line.split(':')
                        self.handle_button_event(button, state)
                        
            except serial.SerialException as e:
                logger.error(f'Serial error: {e}')
                break
            except KeyboardInterrupt:
                logger.info('Shutting down...')
                break
                
        if self.ser and self.ser.is_open:
            self.ser.close()

def main():
    parser = argparse.ArgumentParser(description='Serial to Keyboard')
    parser.add_argument(
        'port',
        nargs='?',
        default='/dev/tty.usbmodem744DBD7D50D02',
        help='Serial port (e.g., COM3 on Windows or /dev/ttyUSB0 on Linux/Mac)')
    parser.add_argument('--baud', type=int, default=115200, help='Baud rate (default: 9600)')
    args = parser.parse_args()

    controller = ArduinoController(args.port, args.baud)
    controller.run()

if __name__ == '__main__':
    main()