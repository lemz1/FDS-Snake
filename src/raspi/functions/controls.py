import serial
import time


SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200


print(f"Successfully connected to serial port {SERIAL_PORT}")


time.sleep(1)
try:
    ser = None
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    print(f"Successfully connected to serial port {SERIAL_PORT}")
    time.sleep(1)

except Exception as e:
    print("Serial port error:", e)
    print(f"Serial port error on {SERIAL_PORT}: {e}")
    print("Proceeding without serial input.")
    ser = None


def read_button_input():
    if ser and ser.in_waiting:
        try:
            line = ser.readline().decode("utf-8").strip()
            line = ser.readline().decode("utf-8", errors="ignore").strip()
            if line in ("LEFT", "DOWN", "UP", "RIGHT"):
                return line
        except Exception as e:
            return None

    return None
