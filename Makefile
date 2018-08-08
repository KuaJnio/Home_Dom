BUILD="docker build --pull -t registry:5000/"
PUSH="docker push registry:5000/"
PULL="docker pull registry:5000/"
TARGET="192.168.1.13"
REMOTE="docker -H $(TARGET):2375"

default:

deploy-common:
	cp common/MQTTClient.py actionmanager/source
	cp common/MQTTClient.py homevents/source
	cp common/MQTTClient.py enocean/source
	cp common/MQTTClient.py hometts/source
	cp common/MQTTClient.py lifx/source
	cp common/MQTTClient.py recorder/source
	cp common/MQTTClient.py webapp/source

	cp common/get_config.py actionmanager/source
	cp common/get_config.py homevents/source
	cp common/get_config.py enocean/source
	cp common/get_config.py hometts/source
	cp common/get_config.py lifx/source
	cp common/get_config.py recorder/source
	cp common/get_config.py webapp/source

clean-target:
	$(TARGET) rm -f mqtt config actionmanager enocean homevents hometts lifx recorder webapp ||:

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
	"$(PULL)mqtt"
	$(TARGET) run -d --restart always --name mqtt -p 1883:1883 -p 1884:1884 registry:5000/mqtt

mqtt:
	make build-mqtt
	make run-mqtt

build-config:
	"$(BUILD)config" config
	"$(PUSH)config"

run-config:
	$(TARGET) rm -f config ||:
	"$(PULL)config"
	$(TARGET) run -d --restart always --name config -p 8090:80 registry:5000/config

config:
	make build-config
	make run-config

build-actionmanager:
	"$(BUILD)actionmanager" actionmanager
	"$(PUSH)actionmanager"

run-actionmanager:
	$(TARGET) rm -f actionmanager ||:
	"$(PULL)actionmanager"
	$(TARGET) run -d --restart always --name actionmanager registry:5000/actionmanager

actionmanager:
	make build-actionmanager
	make run-actionmanager

build-enocean:
	"$(BUILD)enocean" enocean
	"$(PUSH)enocean"

run-enocean:
	$(TARGET) rm -f enocean ||:
	"$(PULL)enocean"
	$(TARGET) run -d --restart always --name enocean --device /dev/ttyUSB0:/dev/ttyENOCEAN registry:5000/enocean

enocean:
	make build-enocean
	make run-enocean

build-hometts:
	"$(BUILD)hometts" hometts
	"$(PUSH)hometts"

run-hometts:
	$(TARGET) rm -f hometts ||:
	"$(PULL)hometts"
	$(TARGET) run -d --restart always --name hometts --device /dev/snd registry:5000/hometts

hometts:
	make build-hometts
	make run-hometts

build-homevents:
	"$(BUILD)homevents" homevents
	"$(PUSH)homevents"

run-homevents:
	$(TARGET) rm -f homevents ||:
	"$(PULL)homevents"
	$(TARGET) run -d --restart always --name homevents registry:5000/homevents

homevents:
	make build-homevents
	make run-homevents

build-lifx:
	"$(BUILD)lifx" lifx
	"$(PUSH)lifx"

run-lifx:
	$(TARGET) rm -f lifx ||:
	"$(PULL)lifx"
	$(TARGET) run -d --restart always --name lifx --net host registry:5000/lifx

lifx:
	make build-lifx
	make run-lifx

build-recorder:
	"$(BUILD)recorder" recorder
	"$(PUSH)recorder"

run-recorder:
	$(TARGET) rm -f recorder ||:
	"$(PULL)recorder"
	$(TARGET) run -d --restart always --name recorder -v /usr/share/recorder-data:/home -p 8000:80 registry:5000/recorder

recorder:
	make build-recorder
	make run-recorder

build-webapp:
	"$(BUILD)webapp" webapp
	"$(PUSH)webapp"

run-webapp:
	$(TARGET) rm -f webapp ||:
	"$(PULL)webapp"
	$(TARGET) run -d --restart always --name webapp -p 80:80 registry:5000/webapp

webapp:
	make build-webapp
	make run-webapp

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

run:
	make run-mqtt
	make run-config
	make run-actionmanager
	make run-enocean
	make run-hometts
	make run-homevents
	make run-lifx
	make run-recorder
	make run-webapp

all:
	make clean-target
	make build
	make run