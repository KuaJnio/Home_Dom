#!/bin/bash

cd mqtt && ./amd64_build.sh && cd ..
cd actionmanager && ./amd64_build.sh && cd ..
cd enocean && ./amd64_build.sh && cd ..
cd lifx && ./amd64_build.sh && cd ..
cd hometts && ./amd64_build.sh && cd ..
