var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function () {
    socket.emit('analysisConnect', { data: 'connected' });
});

function sendData(){
    socket.emit('requestAnalysisData', {data: 'hello'});
};
setInterval(sendData,5000)

socket.on('returnAnalysisData', function (data) {
    for (a in data) {
        if (document.getElementById(a + "Analysis")) {
            var dt = new Date()
            var newLabel = String(dt.getHours()) + ':' + String(dt.getMinutes()) + ':' + String(dt.getSeconds())
            var randomValue = Math.floor((Math.random() * 10) + 1)
            var labelLength = tempChart.data.labels

            addData(tempChart, newLabel, randomValue)
            addData(phChart, newLabel, randomValue)
            if (labelLength.length > 6 ) {
                removeData(tempChart)
                removeData(phChart)
            }
        }
    }
});

//
// live data chart section
//

var tempChartid = document.getElementById('temperatureChart').getContext('2d');
var tempChart = new Chart(tempChartid, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Temperature',
            borderColor: '#50509f',
            data: []
        }]
    },
    options: {}
});

var phChartid = document.getElementById('phChart').getContext('2d');
var phChart = new Chart(phChartid, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'PH',
            borderColor: '#50509f',
            data: []
        }]
    },
    options: {}
});

var wfChartid = document.getElementById('wfChart').getContext('2d');
var wfChart = new Chart(wfChartid, {
    type: 'line',
    data: {
        labels: ['may','june','july'],
        datasets: [{
            label: 'Waterflow',
            borderColor: '#50509f',
            data: [3,4,5]
        }]
    },
    options: {}
});

var clarityChartid = document.getElementById('clarityChart').getContext('2d');
var clarityChart = new Chart(clarityChartid, {
    type: 'line',
    data: {
        labels: ['may','june','july'],
        datasets: [{
            label: 'Water Clarity',
            borderColor: '#50509f',
            data: [3,4,5]
        }]
    },
    options: {}
});

//
// Functions for adding or removing data from charts
//
function addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
    console.log('chart updated')
}

function removeData(c) {
    c.data.labels.shift();
    c.data.datasets.forEach((dataset) => {
        dataset.data.shift();
    });
    c.update();
}

//
// functions for swapping tabs
//
function openCity(evt, cityName) {
    var i, x, tablinks;
    x = document.getElementsByClassName("dataSection");
    for (i = 0; i < x.length; i++) {
      x[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < x.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" w3-border-red", "");
    }
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.firstElementChild.className += " w3-border-red";
  }

