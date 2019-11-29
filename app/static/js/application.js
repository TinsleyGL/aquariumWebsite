var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function() {
    socket.emit('client_connected', {data: 'connected'});
});

function sendData(){
    socket.emit('sendData', {data: 'Request'});
};

setInterval(sendData,5000)
socket.on('data' ,function(data){
    for (a in data) {
        if (document.getElementById(a + "temperature")) {
            if (data[a].temp != document.getElementById(a + "temperature").innerHTML ) {
                tableUpdater('temp', data[a].temp)
            }
            document.getElementById(a + "temperature").innerHTML = data[a].temp;
        }
        if (document.getElementById(a + "ph")) {
            if (data[a].ph != document.getElementById(a + "ph").innerHTML){
                tableUpdater('ph', data[a].ph)
            }
            document.getElementById(a + "ph").innerHTML = data[a].ph;
        }
        if (document.getElementById(a + "FilterFlow")) {
            if (data[a].filterFlow != document.getElementById(a + "FilterFlow").innerHTML) {
                tableUpdater('flow', data[a].filterFlow)
            }
            document.getElementById(a + "FilterFlow").innerHTML = data[a].filterFlow;
        }
        if (document.getElementById(a + "Clarity")) {
            if (data[a].clarity != document.getElementById(a + "Clarity").innerHTML) {
                tableUpdater('clarity', data[a].clarity)
            }
            document.getElementById(a + "Clarity").innerHTML = data[a].clarity;
            if (data[a].clarity > 4) {
                document.getElementById('clarityNote').innerHTML = 'Water Clarity - Clear';
            } else {
                document.getElementById('clarityNote').innerHTML = 'Water Clarity - Cloudy';
            }
        }
    }
});

function tableUpdater(type, data){
    var dt = new Date()
    var label = String(dt.getHours()) + ':' + String(dt.getMinutes()) + ':' + String(dt.getSeconds())
    if (type == 'temp') {
        document.getElementById('tempTableUpdate').innerHTML = "Change in temperature: " + data;
        document.getElementById('tempTableTime').innerHTML  = label
    } else if (type == 'ph') {
        document.getElementById('phTableUpdate').innerHTML = "Change in pH: " + data; 
        document.getElementById('phTableTime').innerHTML = label
    } else if (type == 'flow') {
        document.getElementById('wfTableUpdate').innerHTML = "Change in filter flow: " + data; 
        document.getElementById('wfTableTime').innerHTML = label;
    } else if (type == 'clarity') {
        document.getElementById('clarityTableUpdate').innerHTML = "Change in water clarity: " + data; 
        document.getElementById('clarityTableTime').innerHTML = label;
    }
}