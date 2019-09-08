
var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function() {
    // we emit a connected message to let knwo the client that we are connected.
    socket.emit('client_connected', {data: 'New client!'});
});

function sendData(){
    socket.emit('sendData', {data: 'hello'});
};
setInterval(sendData,5000)

function myFunc() {
    console.log(name)
}

socket.on('data' ,function(data){
    console.log(data);
    //document.getElementById("temperature").innerHTML = data.temp;
    //document.getElementById("ph").innerHTML = data.ph;
});

