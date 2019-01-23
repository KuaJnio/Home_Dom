.PHONY: actionmanager base common config discordinho enocean hometts homevents lifx mqtt recorder weather webapp
BUILD="docker build --pull -t registry:5000/"
PUSH="docker push registry:5000/"
PULL="pull registry:5000/"
HOST="192.168.1.16"
TARGET=docker -H $(HOST):2375

default:

deploy-common:
	cp common/MQTTClient.py actionmanager/source
	cp common/MQTTClient.py homevents/source
	cp common/MQTTClient.py enocean/source
	cp common/MQTTClient.py hometts/source
	cp common/MQTTClient.py lifx/source
	cp common/MQTTClient.py recorder/source
	cp common/MQTTClient.py webapp/source
	cp common/MQTTClient.py weather/source
	cp common/MQTTClient.py discordinho/source
	cp common/MQTTClient.py config/source

	cp common/get_config.py actionmanager/source
	cp common/get_config.py homevents/source
	cp common/get_config.py enocean/source
	cp common/get_config.py hometts/source
	cp common/get_config.py lifx/source
	cp common/get_config.py recorder/source
	cp common/get_config.py webapp/source
	cp common/get_config.py weather/source
	cp common/get_config.py discordinho/source

	cp common/homedom_logger.py actionmanager/source
	cp common/homedom_logger.py homevents/source
	cp common/homedom_logger.py enocean/source
	cp common/homedom_logger.py hometts/source
	cp common/homedom_logger.py lifx/source
	cp common/homedom_logger.py recorder/source
	cp common/homedom_logger.py webapp/source
	cp common/homedom_logger.py weather/source
	cp common/homedom_logger.py discordinho/source
	cp common/homedom_logger.py config/source

clean-target:
	$(TARGET) rm -f mqtt config actionmanager enocean homevents hometts lifx recorder webapp weather discordinho ||:

build-base:
	"$(BUILD)base" base
	"$(PUSH)base"

base:
	make build-base

build-mqtt:
	"$(BUILD)mqtt" mqtt
	"$(PUSH)mqtt"

run-mqtt:
	$(TARGET) rm -f mqtt ||:
	$(TARGET) pull registry:5000/mqtt
	$(TARGET) run --init -d --restart always --name mqtt -p 1883:1883 -p 1884:1884 registry:5000/mqtt

mqtt:
	make build-mqtt
	make run-mqtt

build-config:
	"$(BUILD)config" config
	"$(PUSH)config"

run-config:
	$(TARGET) rm -f config ||:
	$(TARGET) pull registry:5000/config
	$(TARGET) run --init -d --restart always --name config -p 8090:80 -v /mnt/disk/logs:/var/log/homedom registry:5000/config

config:
	make build-config
	make run-config

build-actionmanager:
	"$(BUILD)actionmanager" actionmanager
	"$(PUSH)actionmanager"

run-actionmanager:
	$(TARGET) rm -f actionmanager ||:
	$(TARGET) pull registry:5000/actionmanager
	$(TARGET) run --init -d --restart always --name actionmanager -v /mnt/disk/logs:/var/log/homedom registry:5000/actionmanager

actionmanager:
	make build-actionmanager
	make run-actionmanager

build-enocean:
	"$(BUILD)enocean" enocean
	"$(PUSH)enocean"

run-enocean:
	$(TARGET) rm -f enocean ||:
	$(TARGET) pull registry:5000/enocean
	$(TARGET) run --init -d --restart always --name enocean --device /dev/ttyUSB0:/dev/ttyENOCEAN -v /mnt/disk/logs:/var/log/homedom registry:5000/enocean

enocean:
	make build-enocean
	make run-enocean

build-hometts:
	"$(BUILD)hometts" hometts
	"$(PUSH)hometts"

run-hometts:
	$(TARGET) rm -f hometts ||:
	$(TARGET) pull registry:5000/hometts
	$(TARGET) run --init -d --restart always --name hometts --device /dev/snd -v /mnt/disk/logs:/var/log/homedom registry:5000/hometts

hometts:
	make build-hometts
	make run-hometts

build-homevents:
	"$(BUILD)homevents" homevents
	"$(PUSH)homevents"

run-homevents:
	$(TARGET) rm -f homevents ||:
	$(TARGET) pull registry:5000/homevents
	$(TARGET) run --init -d --restart always --name homevents -p 8080:80 -v /mnt/disk/logs:/var/log/homedom registry:5000/homevents

homevents:
	make build-homevents
	make run-homevents

build-lifx:
	"$(BUILD)lifx" lifx
	"$(PUSH)lifx"

run-lifx:
	$(TARGET) rm -f lifx ||:
	$(TARGET) pull registry:5000/lifx
	$(TARGET) run --init -d --restart always --name lifx --net host -v /mnt/disk/logs:/var/log/homedom registry:5000/lifx

lifx:
	make build-lifx
	make run-lifx

build-recorder:
	"$(BUILD)recorder" recorder
	"$(PUSH)recorder"

run-recorder:
	$(TARGET) rm -f recorder ||:
	$(TARGET) pull registry:5000/recorder
	$(TARGET) run --init -d --restart always --name recorder -v /mnt/disk/recorder-data:/home -p 8000:80 -v /mnt/disk/logs:/var/log/homedom registry:5000/recorder

recorder:
	make build-recorder
	make run-recorder

build-webapp:
	"$(BUILD)webapp" webapp
	"$(PUSH)webapp"

run-webapp:
	$(TARGET) rm -f webapp ||:
	$(TARGET) pull registry:5000/webapp
	$(TARGET) run --init -d --restart always --name webapp -p 80:80 -v /mnt/disk/logs:/var/log/homedom registry:5000/webapp

webapp:
	make build-webapp
	make run-webapp

build-weather:
	"$(BUILD)weather" weather
	"$(PUSH)weather"

run-weather:
	$(TARGET) rm -f weather ||:
	$(TARGET) pull registry:5000/weather
	$(TARGET) run --init -d --restart always --name weather -v /mnt/disk/logs:/var/log/homedom registry:5000/weather

weather:
	make build-weather
	make run-weather

build-discordinho:
	"$(BUILD)discordinho" discordinho
	"$(PUSH)discordinho"

run-discordinho:
	$(TARGET) rm -f discordinho ||:
	$(TARGET) pull registry:5000/discordinho
	$(TARGET) run --init -d --restart always --name discordinho -v /mnt/disk/logs:/var/log/homedom registry:5000/discordinho

discordinho:
	make build-discordinho
	make run-discordinho

build:
	make deploy-common
	make build-base
	make build-mqtt
	make build-config
	make build-actionmanager
	make build-enocean
	make build-hometts
	make build-homevents
	make build-lifx
	make build-recorder
	make build-webapp
	make build-weather
	make build-discordinho

run:
	make run-mqtt
	make run-config
	sleep 3
	make run-actionmanager
	make run-enocean
	make run-hometts
	make run-homevents
	make run-lifx
	make run-recorder
	make run-webapp
	make run-weather
	make run-discordinho

all:
	make clean-target
	make build
	make run
