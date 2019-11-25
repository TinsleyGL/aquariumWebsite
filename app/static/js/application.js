var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function() {
    // we emit a connected message to let knwo the client that we are connected.
    socket.emit('client_connected', {data: 'connected'});
});

function sendData(){
    socket.emit('sendData', {data: 'Request'});
};
setInterval(sendData,5000)

socket.on('data' ,function(data){
    for (a in data) {
        if (document.getElementById(a + "temperature")) {
            document.getElementById(a + "temperature").innerHTML = data[a].temp;
        }
        if (document.getElementById(a + "ph")) {
            document.getElementById(a + "ph").innerHTML = data[a].ph;
        }
        if (document.getElementById(a + "FilterFlow")) {
            document.getElementById(a + "FilterFlow").innerHTML = data[a].filterFlow;
        }
        if (document.getElementById(a + "Clarity")) {
            document.getElementById(a + "Clarity").innerHTML = data[a].clarity;
        }
    }
});

