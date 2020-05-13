// Create a client instance
client = new Paho.MQTT.Client("192.168.1.14", 1884, "WebApp");

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

function appOn(app) {
    $(`.${app}`).removeClass("has-background-danger");
    $(`.${app}`).addClass("has-background-primary");
}

function appOff(app) {
    $(`.${app}`).removeClass("has-background-primary");
    $(`.${app}`).addClass("has-background-danger");
}

// called when a message arrives
function onMessageArrived(message) {
    //console.log("onMessageArrived:"+message.payloadString);
    if (message.destinationName == "status") {
        appOn(message.payloadString);
    }
}

$( ".on" ).click(function() {
    time = new Date().getTime() / 1000;
    message = new Paho.MQTT.Message(JSON.stringify({"HD_FEATURE": "HD_BUTTON", "HD_IDENTIFIER": this.id, "HD_VALUE": 1, "HD_TIMESTAMP": time}));
    message.destinationName = "inputs";
    client.send(message);
});

$( ".off" ).click(function() {
    time = new Date().getTime() / 1000;
    message = new Paho.MQTT.Message(JSON.stringify({"HD_FEATURE": "HD_BUTTON", "HD_IDENTIFIER": this.id, "HD_VALUE": 0, "HD_TIMESTAMP": time}));
    message.destinationName = "inputs";
    client.send(message);
});


