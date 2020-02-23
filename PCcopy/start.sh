#!/bin/bash

# Replace Ip address with raspberry pi
python3 detect.py & ssh pi@(replace_ip) & ./runme.sh 


