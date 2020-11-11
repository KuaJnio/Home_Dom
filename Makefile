.PHONY: actionmanager base common config discordinho enocean hometts homevents lifx mqtt recorder weather webapp
REGISTRY=registry.romain-dupont.fr
BUILD="docker build --pull -t $(REGISTRY)/"
PUSH="docker push $(REGISTRY)/"
PULL="pull $(REGISTRY)/"
HOST="192.168.1.37"
TARGET=docker -H $(HOST):2375
LOGDIR=/data/home_dom/logs

default:
	make all

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
	docker image prune -f

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
	$(TARGET) pull $(REGISTRY)/mqtt
	$(TARGET) run --init -d --restart always --name mqtt -p 1883:1883 -p 1884:1884 $(REGISTRY)/mqtt

mqtt:
	make build-mqtt
	make run-mqtt

build-config:
	"$(BUILD)config" config
	"$(PUSH)config"

run-config:
	$(TARGET) rm -f config ||:
	$(TARGET) pull $(REGISTRY)/config
	$(TARGET) run --init -d --restart always --name config -p 8090:80 -v $(LOGDIR):/var/log/homedom $(REGISTRY)/config

config:
	make build-config
	make run-config

build-actionmanager:
	"$(BUILD)actionmanager" actionmanager
	"$(PUSH)actionmanager"

run-actionmanager:
	$(TARGET) rm -f actionmanager ||:
	$(TARGET) pull $(REGISTRY)/actionmanager
	$(TARGET) run --init -d --restart always --name actionmanager -v $(LOGDIR):/var/log/homedom $(REGISTRY)/actionmanager

actionmanager:
	make build-actionmanager
	make run-actionmanager

build-enocean:
	"$(BUILD)enocean" enocean
	"$(PUSH)enocean"

run-enocean:
	$(TARGET) rm -f enocean ||:
	$(TARGET) pull $(REGISTRY)/enocean
	$(TARGET) run --init -d --restart always --name enocean --device /dev/ttyUSB0:/dev/ttyENOCEAN -v $(LOGDIR):/var/log/homedom $(REGISTRY)/enocean

enocean:
	make build-enocean
	make run-enocean

enocean-debug:
	make clean-target
	make deploy-common
	make build-base
	make mqtt
	make config
	sleep 3
	make enocean

build-hometts:
	"$(BUILD)hometts" hometts
	"$(PUSH)hometts"

run-hometts:
	$(TARGET) rm -f hometts ||:
	$(TARGET) pull $(REGISTRY)/hometts
	$(TARGET) run --init -d --restart always --name hometts --device /dev/snd -v $(LOGDIR):/var/log/homedom $(REGISTRY)/hometts

hometts:
	make build-hometts
	make run-hometts

build-homevents:
	"$(BUILD)homevents" homevents
	"$(PUSH)homevents"

run-homevents:
	$(TARGET) rm -f homevents ||:
	$(TARGET) pull $(REGISTRY)/homevents
	$(TARGET) run --init -d --restart always --name homevents -p 8080:80 -v $(LOGDIR):/var/log/homedom --memory="1g" --memory-swap="2g" $(REGISTRY)/homevents

homevents:
	make build-homevents
	make run-homevents

build-lifx:
	"$(BUILD)lifx" lifx
	"$(PUSH)lifx"

run-lifx:
	$(TARGET) rm -f lifx ||:
	$(TARGET) pull $(REGISTRY)/lifx
	$(TARGET) run --init -d --restart always --name lifx --net host -v $(LOGDIR):/var/log/homedom $(REGISTRY)/lifx

lifx:
	make build-lifx
	make run-lifx

build-recorder:
	"$(BUILD)recorder" recorder
	"$(PUSH)recorder"

run-recorder:
	$(TARGET) rm -f recorder ||:
	$(TARGET) pull $(REGISTRY)/recorder
	$(TARGET) run --init -d --restart always --name recorder -v /mnt/disk/recorder-data:/home -p 8000:80 -v $(LOGDIR):/var/log/homedom $(REGISTRY)/recorder

recorder:
	make build-recorder
	make run-recorder

build-webapp:
	"$(BUILD)webapp" webapp
	"$(PUSH)webapp"

run-webapp:
	$(TARGET) rm -f webapp ||:
	$(TARGET) pull $(REGISTRY)/webapp
	$(TARGET) run --init -d --restart always --name webapp -p 80:80 -v $(LOGDIR):/var/log/homedom $(REGISTRY)/webapp

webapp:
	make build-webapp
	make run-webapp

build-weather:
	"$(BUILD)weather" weather
	"$(PUSH)weather"

run-weather:
	$(TARGET) rm -f weather ||:
	$(TARGET) pull $(REGISTRY)/weather
	$(TARGET) run --init -d --restart always --name weather -v $(LOGDIR):/var/log/homedom $(REGISTRY)/weather

weather:
	make build-weather
	make run-weather

build-discordinho:
	"$(BUILD)discordinho" discordinho
	"$(PUSH)discordinho"

run-discordinho:
	$(TARGET) rm -f discordinho ||:
	$(TARGET) pull $(REGISTRY)/discordinho
	$(TARGET) run --init -d --restart always --name discordinho -v $(LOGDIR):/var/log/homedom $(REGISTRY)/discordinho

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
	#make run-discordinho

logs:
	tail -f $(LOGDIR)/* ||:

all:
	make clean-target
	make build
	make run
