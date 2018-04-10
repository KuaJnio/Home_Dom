#!/bin/bash

#cd mqtt && ./build.sh && cd ..
cd actionmanager && ./build.sh && cd ..
cd enocean && ./build.sh && cd ..
cd lifx && ./build.sh && cd ..
cd hometts && ./build.sh && cd ..
cd recorder && ./build.sh && cd ..
#cd cep && ./build.sh && cd ..
cd webapp && ./build.sh && cd ..

docker rmi $(docker images | grep "<none>" | awk '{print $3}')

ssh pi@homedom-armhf-touch /home/pi/clean.sh
