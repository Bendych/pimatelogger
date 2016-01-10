# pimatelogger
This is my try at a climate logger script that runs on a Raspberry Pi

## What it does
It reads the Temperature and Humidity values from a Sensor like the DHT22, stores it in an RRD file and generates the appropriate graphs.

## What you need
- a Raspberry Pi
- a DHT22 or similar Sensor
- the corresponding driver installed

## Installation
WARNING: This is still very un-finished :)

- Install the Driver for the AM2302 sensor (Instructions: https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/software-install-updated)
- install rrdtool and its python integration (sudo apt-get rrdtool python-rrd)
- install this script

If you want to serve the graphs via HTTP, then
- install apache

If you want to use the device with a local display (This is still work in progress)
- install chromium

## Configuration
All configuration is done in the Head portion of the Python-Script.
