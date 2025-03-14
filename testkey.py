import serial
import pyautogui
import time

# Open serial connection
arduino = serial.Serial('/dev/tty.usbmodem744DBD7D50D02', 115200, timeout=1)
time.sleep(2)  # Allow connection to establish

while True:
    if arduino.in_waiting > 0:
        command = arduino.readline().decode('utf-8').strip()
        
        if command == "A":
            pyautogui.hotkey('A')
        elif command == "D":
            pyautogui.hotkey('D')