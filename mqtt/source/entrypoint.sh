#!/bin/bash

trap "kill -15 $(jobs -p); exit 0;" SIGTERM SIGINT

/usr/sbin/mosquitto -c /root/mqtt/mosquitto.conf

while :
do
        sleep 1
done
