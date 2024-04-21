# ---------------------------------------------------------------------------
# RTTTL loader for music module.
# 
# Author: Dilshan Jayakody [jayakody2000lk@gmail.com]
# Last updated: 20th April 2024
# ---------------------------------------------------------------------------

import sys
import serial
import time
import argparse


def extract_tone_info(rtttl_str):
    # Check for empty string.
    if len(rtttl_str) < 1:
        print("Error: No RTTTL data found or invalid file")
        return None, None

    # Extract name from the RTTTL data.
    rtttl_name = rtttl_str.split(':')[0]

    # Remove name from the RTTTL data.
    rtttl_name_len = len(rtttl_name)
    rtttl_data = (rtttl_str[rtttl_name_len:]).strip()

    # Check for name seperator [:] and remove if exists.
    if rtttl_data[0] == ':':
        rtttl_data = (rtttl_data[1:]).strip()

    # Remove [,] from the end of the file.
    if rtttl_data[len(rtttl_data) - 1] == ',':
        rtttl_data = rtttl_data[:len(rtttl_data) - 1]

    return rtttl_name, rtttl_data


def main():
    # Set default communication port based on the operating system.
    if sys.platform == 'win32':
        default_port = "COM3"
    else:
        default_port = "ttyUSB0"

    # Commandline argument processor.
    parser = argparse.ArgumentParser(description="Music module - RTTTL file transfer utility.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", "--port", default=default_port, help="Communication port")
    parser.add_argument("-m", "--mode", help="Specify the read or write mode", choices=['read', 'write'],
                        default='read')
    parser.add_argument("-f", "--file", help="RTTTL Text file", required=True)
    args = vars(parser.parse_args())

    # Extract values specified in through commandline.
    rtttl_file = args["file"]
    comm_port = args["port"]
    op_mode = args["mode"]
    
    # Set path of the communication port.
    comm_port_path = comm_port
    if sys.platform != 'win32':
        comm_port_path = '/dev/' + comm_port
        
    if op_mode == 'write':
        # Read RTTTL data from the specified file.
        rtttl = open(rtttl_file, "r")
        rtttl_data = rtttl.read()
        rtttl.close()

        # Extract RTTTL name and tone data from the file.
        data_name, tone_data = extract_tone_info(rtttl_data.strip())

        # Check for valid RTTTL data.
        if len(tone_data) < 2:
            print("Unable to find RTTTL data in the specified file")
            return

        # Check RTTTL data is fit with EEPROM size.
        if len(tone_data) > 0xFE:
            print("Specified RTTTL data is too large for EEPROM")
            return
        
        # Open serial connection with the music module.
        serial_con = serial.Serial(comm_port_path, 115200)

        # Write specified RTTTL data into the music module.
        serial_con.write([0x65])
        time.sleep(0.2)

        for temp_char in tone_data:
            serial_con.write(temp_char.encode())
            time.sleep(0.005)

        # End of RTTTL data transfer.
        serial_con.write([0x1B])
        serial_con.close()

    elif op_mode == 'read':
        # Open serial connection with the music module.
        serial_con = serial.Serial(comm_port_path, 115200)

        # Send read request to the music controller.
        serial_con.write([0x72])
        time.sleep(0.2)

        # Read all available data in the serial buffer.
        rtttl_data = serial_con.read_until(b'\x00')
        serial_con.close()

        if len(rtttl_data) > 2:
            # Remove NULL character at the end of the received data buffer.
            if rtttl_data[len(rtttl_data) - 1] == 0:
                rtttl_data = rtttl_data[:-1]

            rtttl_str = rtttl_data.decode('utf8')
            # Append name into the RTTTL data.
            rtttl_str = 'untitled:' + rtttl_str

            # Write data into the specified file.
            rtttl = open(rtttl_file, "w")
            rtttl.write(rtttl_str)
            rtttl.close()
        else:
            print("No RTTTL data received from the music module")


if __name__ == '__main__':
    main()
