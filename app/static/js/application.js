var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function() {
    // we emit a connected message to let knwo the client that we are connected.
    socket.emit('client_connected', {data: 'connected'});
});

function sendData(){
    socket.emit('sendData', {data: 'hello'});
};
setInterval(sendData,5000)

socket.on('data' ,function(data){
    for (a in data) {
        if (document.getElementById(a + "temperature")) {
            document.getElementById(a + "temperature").innerHTML = data[a].temp;
            console.log(a)
            console.log(data[a].temp)
        }
        if (document.getElementById(a + "ph")) {
            document.getElementById(a + "ph").innerHTML = data[a].ph;
            console.log(a)
            console.log(data[a].ph)
        }
    }
});

