#!/bin/bash

cd mqtt && ./armhf_build.sh && cd ..
cd actionmanager && ./armhf_build.sh && cd ..
cd enocean && ./armhf_build.sh && cd ..
cd lifx && ./armhf_build.sh && cd ..
cd hometts && ./armhf_build.sh && cd ..
cd recorder && ./armhf_build.sh && cd ..
