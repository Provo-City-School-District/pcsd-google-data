#!/bin/bash

source /docker/pcsd-google-data/google-data/bin/activate
cd /tmp
python3 /docker/pcsd-google-data/main.py
rm all_devices.json