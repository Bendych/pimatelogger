# pimatelogger
This is my try at a climate logger script that runs on a Raspberry Pi

## What it does
It reads the Temperature and Humidity values from a Sensor like the DHT22, stores it in an RRD file and generates the appropriate graphs.

## What you need
- a Raspberry Pi
- a DHT22 or similar Sensor
- the corresponding driver installed

## Installation
- Install the Driver for the AM2302 sensor (Instructions: https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/software-install-updated)
- install rrdtool and its python integration (sudo apt-get rrdtool python-rrd)
- install apache (sudo apt-get apache2)
- install this script (git clone https://github.com/Bendych/pimatelogger.git)

- add the following line to the file /etc/rc.local right above *exit 0* (create if it doesn't exist)
python /home/pi/templogger/templogger.py&

If you want to use the device with a local display (This is still work in progress)
- install chromium (sudo apt-get chromium)

## Configuration
All configuration is done in the Head portion of the Python-Script.

Now reboot your Raspberry Pi to have it start logging
