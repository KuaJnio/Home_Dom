container_ip = "localhost"

var meteo_title = document.getElementsByClassName("meteo_title")[0];
var meteo_temperature = document.getElementsByClassName("meteo_temperature")[0];
var meteo_humidity = document.getElementsByClassName("meteo_humidity")[0];
var meteo_rssi = document.getElementsByClassName("meteo_rssi")[0];
var meteo_date = document.getElementsByClassName("meteo_date")[0];

var contact_title = document.getElementsByClassName("contact_title")[0];
var contact_contact = document.getElementsByClassName("contact_contact")[0];
var contact_rssi = document.getElementsByClassName("contact_rssi")[0];
var contact_date = document.getElementsByClassName("contact_date")[0];

var relay_title = document.getElementsByClassName("relay_title")[0];
var relay_channel_1 = document.getElementsByClassName("relay_on")[0];
var relay_channel_2 = document.getElementsByClassName("relay_off")[0];
var relay_rssi = document.getElementsByClassName("relay_rssi")[0];
var relay_date = document.getElementsByClassName("relay_date")[0];

var lifx_title = document.getElementsByClassName("lifx_title")[0];
var lifx_on = document.getElementsByClassName("lifx_on")[0];
var lifx_off = document.getElementsByClassName("lifx_off")[0];
var lifx_color_r = document.getElementsByClassName("lifx_color_r")[0];
var lifx_color_g = document.getElementsByClassName("lifx_color_g")[0];
var lifx_color_b = document.getElementsByClassName("lifx_color_b")[0];
var lifx_intensity = document.getElementsByClassName("lifx_intensity")[0];

function parse_payload(payload) {
	var parsed_payload=JSON.parse(payload);
	var type = parsed_payload['type'];
	var teachIn = parsed_payload['TeachIn'];
	var d = new Date();
	relay_date.value = d;
	if ((type == 'TEMPERATURE') && (teachIn == false)) {
		meteo_temperature.value = parsed_payload['temperature'];
		meteo_humidity.value = parsed_payload['humidity'];
		

	}
		else if ((type == 'CONTACT') && (teachIn == 'false')) {
		contact_contact.value = parsed_payload['state'];
	}
}

function connect_enocean_ws(){
    try {
        var host = "ws://"+container_ip+":8081/ws";
        console.log("Host:", host);
        var ws = new WebSocket(host);

        ws.onopen = function (e) {
            console.log("Socket opened");
        };

        ws.onclose = function (e) {
            console.log("Socket closed");
            setTimeout(function(){connect_enocean_ws()}, 5000);
        };

        ws.onmessage = function (e) {
            var payload = JSON.stringify(JSON.parse(e.data), null, 2);
            console.log("Socket message:\n", payload);
            parse_payload(e.data);
        };

        ws.onerror = function (e) {
            console.log("Socket error:", e);
        };
    } catch (ex) {
        console.log("Socket exception:", ex);
    }
}

connect_enocean_ws();

