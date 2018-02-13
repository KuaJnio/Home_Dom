// Create a client instance
client = new Paho.MQTT.Client("192.168.1.13", 1884, "WebApp");

// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// connect the client
client.connect({onSuccess:onConnect});


// called when the client connects
function onConnect() {
  // Once a connection has been made, make a subscription and send a message.
  console.log("onConnect");
  client.subscribe("#");
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:"+responseObject.errorMessage);
  }
}

// called when a message arrives
function onMessageArrived(message) {
  console.log("onMessageArrived:"+message.payloadString);
}

function clicked_1() {
  message = new Paho.MQTT.Message(JSON.stringify({"target": "lifx", "power": "on", "color": [58275, 0, 65535, 2500]}));
  message.destinationName = "outputs";
  client.send(message);
}

function clicked_2() {
  message = new Paho.MQTT.Message(JSON.stringify({"target": "lifx", "power": "off", "color": [58275, 0, 65535, 2500]}));
  message.destinationName = "outputs";
  client.send(message);
}

document.getElementsByClassName("1")[0].addEventListener("click", clicked_1, false);

document.getElementsByClassName("2")[0].addEventListener("click", clicked_2, false);
