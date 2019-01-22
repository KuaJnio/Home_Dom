// Create a client instance
client = new Paho.MQTT.Client("192.168.1.16", 1884, "WebApp");

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
    
    if (message.destinationName == "status") {
        if (message.payloadString == actionmanager)
        {
            $(".actionmanager").removeClass("has-background-danger");
            $(".actionmanager").addClass("has-background-primary");
        }
        else if (message.payloadString == config)
        {
            $(".config").removeClass("has-background-danger");
            $(".config").addClass("has-background-primary");
        }
        else if (message.payloadString == weather)
        {
            $(".weather").removeClass("has-background-danger");
            $(".weather").addClass("has-background-primary");
        }
        else if (message.payloadString == webapp)
        {
            $(".webapp").removeClass("has-background-danger");
            $(".webapp").addClass("has-background-primary");
        }
        else if (message.payloadString == homevents)
        {
            $(".homevents").removeClass("has-background-danger");
            $(".homevents").addClass("has-background-primary");
        }
        else if (message.payloadString == discordinho)
        {
            $(".discordinho").removeClass("has-background-danger");
            $(".discordinho").addClass("has-background-primary");
        }
        else if (message.payloadString == enocean)
        {
            $(".enocean").removeClass("has-background-danger");
            $(".enocean").addClass("has-background-primary");
        }
        else if (message.payloadString == lifx)
        {
            $(".lifx").removeClass("has-background-danger");
            $(".lifx").addClass("has-background-primary");
        }
        else if (message.payloadString == recorder)
        {
            $(".recorder").removeClass("has-background-danger");
            $(".recorder").addClass("has-background-primary");
        }
        else if (message.payloadString == hometts)
        {
            $(".hometts").removeClass("has-background-danger");
            $(".hometts").addClass("has-background-primary");
        }
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


