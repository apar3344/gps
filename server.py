from flask import Flask, Response
import serial
import time
import json

app = Flask(__name__)

# Create a context manager for the serial port to ensure it's properly closed
class SerialPort:
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate
        self.serial = None

    def __enter__(self):
        self.serial = serial.Serial(self.port, self.baud_rate)
        return self.serial

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.serial is not None:
            self.serial.close()

def generate_gps_data():
    with SerialPort('/dev/ttyS0', 9600) as ser:
        while True:
            try:
                data = ser.readline().decode('utf-8')
                if data.startswith("$GPGGA"):
                    coordinates = parse_coordinates(data)
                    yield json.dumps(coordinates) + '\n'
            except serial.SerialException as e:
                # Handle the exception, e.g., log the error and continue
                print(f"Serial port error: {e}")
            except Exception as e:
                # Handle other exceptions
                print(f"An error occurred: {e}")
            time.sleep(1)  # Adjust the sleep time as needed

def parse_coordinates(data):
    # Parse the GPS data and extract latitude and longitude
    # Adjust this parsing logic based on your GPS data format.
    parts = data.split(',')
    if len parts) >= 10:
        latitude = parts[2]
        longitude = parts[4]
        return {'latitude': latitude, 'longitude': longitude}
    else:
        return {'latitude': None, 'longitude': None}

# Comment out the Flask route for streaming and displaying the coordinates
# @app.route('/stream_gps')
# def stream_gps():
#     return Response(generate_gps_data(), content_type='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
