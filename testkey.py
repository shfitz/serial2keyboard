# Python Code
import serial
import keyboard

# Set the correct serial port
arduino_port = "/dev/tty.usbmodem744DBD7D50D02"  # Replace with your Arduino's serial port
baud_rate = 115200

# Establish serial connection
try:
    ser = serial.Serial(arduino_port, baud_rate)
    print(f"Connected to {arduino_port} at {baud_rate} baud")
except serial.SerialException as e:
    print(f"Error: {e}")
    exit()

try:
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            if data == "A":
                keyboard.press_and_release('a')
            # Add more conditions for other data and key presses
except KeyboardInterrupt:
    print("Exiting...")
finally:
    ser.close()
    print("Serial port closed")