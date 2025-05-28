# AlpycaDeviceCirPy - Python Alpaca Device Driver SDK for CircuitPython

This project tries to follow the same conventions of the original as close as possible within the contraints of what's available in CircuitPython; As such, many things need to change but should feel similar to the original.


## Instructions

Copy all of the files from the `device` directory onto your CircuitPython device

Install `circup` with `pip`

Use cirup to install `adafruit_logging` (eg. `circup install adafruit_loggin`), `adafruit_httpserver`, `adafruit_connection_manager`, `asyncio`, and `toml`

## Known issues
- UConform fails due to a timeout for 1 test. I've been unable to figure out why as of yet but it shouldn't affect real use
- Discovery can be tempermental and may take multiple searches for the device to show up
- Still working my way through the templates. So far only covercalibrator and rotator have been converted
- Enabling write of log file has not been fully tested. As such, boot.py doesn't mount the filesystem yet.