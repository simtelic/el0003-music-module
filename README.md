# RTTTL loader for music module

This repository contains a Python script (`rttl-loader.py`) that makes it easy to load or view RTTTL data in a music module.

## Requirements
- Python 3 (https://www.python.org/downloads/)
- pyserial library (https://pyserial.readthedocs.io/en/latest/)

##### Install dependencies (Windows)
```
py -m pip install pyserial
```
##### Install dependencies (Linux)
```
pip install pyserial
```

## Usage

#### Clone the repository:
   
```
git clone https://github.com/simtelic/el0003-music-module.git
```

If `git` is not available, download the source code snapshot from [GitHub](https://github.com/simtelic/el0003-music-module/archive/refs/heads/main.zip).

#### Run the script:

##### Windows:
Use a application like *Device Manager* to identify the assigned COM port (e.g., COM3).
```
py rttl-loader.py COM3 # Replace with your actual serial port
```

##### Linux:
Use a tool like `ls /dev/tty*` or `dmesg | grep tty` to find the serial port assigned to your music module. It's typically named `/dev/ttyUSB0`, but it might vary.
```
python3 rttl-loader.py /dev/ttyUSB0  # Replace with your actual serial port
```

## Additional Notes

- The repository contains a large collection of RTTTL files available at [FlipperMusicRTTTL](https://github.com/neverfa11ing/FlipperMusicRTTTL) repository. Most of the files in this repository are working with this module and can fit into a 2Kbit EEPROM space.
