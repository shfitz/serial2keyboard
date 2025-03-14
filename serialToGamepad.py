import serial
import pyvjoy
import time

# Set up serial connection
arduino = serial.Serial('/dev/tty.usbmodem744DBD7D50D02', 115200, timeout=0.1)
time.sleep(2)  # Allow connection to establish

# Set up virtual joystick
joystick = pyvjoy.VJoyDevice(1)  # Device ID 1

while True:
    if arduino.in_waiting > 0:
        try:
            # Read and parse data from Arduino
            data = arduino.readline().decode('utf-8').strip().split(',')
            if len(data) == 2:
                button_a, button_b = data
                
                # Update button states
                joystick.set_button(1, int(button_a))
                joystick.set_button(2, int(button_b))
                
        except Exception as e:
            print(f"Error: {e}")