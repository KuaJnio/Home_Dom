#!/bin/bash

cd mqtt && ./build.sh && cd ..
cd actionmanager && ./build.sh && cd ..
cd enocean && ./build.sh && cd ..
cd lifx && ./build.sh && cd ..
cd hometts && ./build.sh && cd ..
cd recorder && ./build.sh && cd ..
