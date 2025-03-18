#!/bin/bash

source /docker/pcsd-google-data/google-data/bin/activate
cd /docker/pcsd-google-data/
python3 /docker/pcsd-google-data/main.py
rm all_devices.json