
var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function() {
    // we emit a connected message to let knwo the client that we are connected.
    socket.emit('client_connected', {data: 'New client!'});
});

function sendData(){
    socket.emit('sendData', {data: 'hello'});
};

setInterval(sendData,5000)

socket.on('data' ,function(data){
    console.log(data);
});

var g = new JustGage({
    id: "gauge1",
    value: 26,
    min: 0,
    max: 40,
    title: "Temperature"
});

var g = new JustGage({
    id: "gauge2",
    value: 7,
    min: 0,
    max: 14,
    title: "PH"
});

var g = new JustGage({
    id: "gauge3",
    value: 87,
    min: 0,
    max: 100,
    title: "Filter Flow"
});

var g = new JustGage({
    id: "gauge4",
    value: 67,
    min: 0,
    max: 100,
    title: "Water clarity"
});