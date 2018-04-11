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

$( ".on" ).click(function() {
  message = new Paho.MQTT.Message(JSON.stringify({"HD_FEATURE": "HD_BUTTON", "HD_IDENTIFIER": this.id, "HD_VALUE": 1}));
  message.destinationName = "inputs";
  client.send(message);
});

$( ".off" ).click(function() {
  message = new Paho.MQTT.Message(JSON.stringify({"HD_FEATURE": "HD_BUTTON", "HD_IDENTIFIER": this.id, "HD_VALUE": 0}));
  message.destinationName = "inputs";
  client.send(message);
});