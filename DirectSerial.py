import serial
import struct
import time

ser1 = serial.Serial("COM8", 115200, timeout=3)
#ser2 = serial.Serial("COM8", 115200, timeout=1)

def send_direct1(token, data):
    # Prepare the data
    if token == 'W':
        # Prepare data packet for 'W' token (as unsigned char)
        in_str = token.encode() + struct.pack('B' * len(data), *data) + '~'.encode()
    else:
        # Different packing structure might be needed for other tokens
        in_str = token.encode() + struct.pack('b' * len(data), *data) + '~'.encode()

    # Send the data
    print(in_str)
    ser1.write(in_str)

    # Wait for the response
    time.sleep(0.5)
    response = ser1.readline()
    return response

def changeLed1(turnon):
    # Prepare the data
    token = "W"
    data = [100, 6, turnon]
    if token == 'W':
        # Prepare data packet for 'W' token (as unsigned char)
        in_str = token.encode() + struct.pack('B' * len(data), *data) + '~'.encode()
    
    # Send the data
    ser1.write(in_str)

    # Return the response
    response = ""
    return response

def encode(in_str, encoding='utf-8'):
    # Encode the input string
    if isinstance(in_str, bytes):
        return in_str
    else:
        return in_str.encode(encoding)

def send_dogcommand1(cmd, duration):
    # Prepare the data
    print(encode(cmd))
    ser1.write(encode(cmd))

    # Wait for the response
    time.sleep(0.5)
    response = ser1.readline()
    time.sleep(duration)
    return response

def send_direct2(token, data):
    # Prepare the data
    if token == 'W':
        # Prepare data packet for 'W' token (as unsigned char)
        in_str = token.encode() + struct.pack('B' * len(data), *data) + '~'.encode()
    else:
        # Different packing structure might be needed for other tokens
        in_str = token.encode() + struct.pack('b' * len(data), *data) + '~'.encode()

    # Send the data
    print(in_str)
    ser1.write(in_str)

    # Wait for the response
    time.sleep(0.5)
    response = ser1.readline()
    return response

# Example usage:
# time.sleep(5)
# response = send_direct1(token, data)
# time.sleep(5)
# data = [100, 6, 0]
# response = send_direct1(token, data)
