TARGET="192.168.1.13"

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

build-base:
	docker build --no-cache --pull -t registry:5000/base base
	docker push registry:5000/base base

build-mqtt:
	docker build --no-cache --pull -t registry:5000/mqtt mqtt
	docker push registry:5000/mqtt

build-actionmanager:
	docker build --no-cache --pull -t registry:5000/actionmanager actionmanager
	docker push registry:5000/actionmanager

build-config:
	docker build --no-cache --pull -t registry:5000/config config
	docker push registry:5000/config

build-enocean:
	docker build --no-cache --pull -t registry:5000/enocean enocean
	docker push registry:5000/enocean

build-hometts:
	docker build --no-cache --pull -t registry:5000/hometts hometts
	docker push registry:5000/hometts

build-homevents:
	docker build --no-cache --pull -t registry:5000/homevents homevents
	docker push registry:5000/homevents

build-lifx:
	docker build --no-cache --pull -t registry:5000/lifx lifx
	docker push registry:5000/lifx

build-recorder:
	docker build --no-cache --pull -t registry:5000/recorder recorder
	docker push registry:5000/recorder

build-webapp:
	docker build --no-cache --pull -t registry:5000/webapp webapp
	docker push registry:5000/webapp

build-apps:
	make deploy-common
	make build-actionmanager
	make build-config
	make build-enocean
	make build-hometts
	make build-homevents
	make build-lifx
	make build-recorder
	make build-webapp
