var weeklyChartD = JSON.parse(document.getElementById("mydiv1").dataset.data1);
var monthlyChartD = JSON.parse(document.getElementById("mydiv2").dataset.data2);
var yearlyChartD = JSON.parse(document.getElementById("mydiv3").dataset.data3);
//console.log(weeklyChartD)
console.log(monthlyChartD)
//console.log(yearlyChartD)
//console.log(Object.values(monthlyChartD['clarity']));

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
            var labelLength = tempChart.data.labels
            try {
                addData(tempChart, newLabel, data[a].temp)
                addData(phChart, newLabel, data[a].ph)
                addData(wfChart, newLabel, data[a].filterFlow)
                addData(clarityChart, newLabel, parseFloat(data[a].clarity))
                console.log(data[a].clarity)
            } catch (error) {
                console.log(error)
            }
            if (labelLength.length > 6 ) {
                removeData(tempChart)
                removeData(phChart)
                removeData(wfChart)
                removeData(clarityChart)
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
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    suggestedMin: 0,
                    suggestedMax: 35
                }
            }]
        }
    }
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
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    suggestedMin: 0,
                    suggestedMax: 14
                }
            }]
        }
    }
});

var wfChartid = document.getElementById('wfChart').getContext('2d');
var wfChart = new Chart(wfChartid, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Waterflow',
            borderColor: '#50509f',
            data: []
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    suggestedMin: 0,
                    suggestedMax: 100
                }
            }]
        }
    }
});

var clarityChartid = document.getElementById('clarityChart').getContext('2d');
var clarityChart = new Chart(clarityChartid, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Water Clarity',
            borderColor: '#50509f',
            data: []
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    suggestedMin: 0,
                    suggestedMax: 10
                }
            }]
        }
    }
});


//
// weekly average chart section
//

var tempWeeklyChartid = document.getElementById('temperatureWeeklyChart').getContext('2d');
var tempWeeklyChart = new Chart(tempWeeklyChartid, {
    type: 'bar',
    data: {
        labels: ['Monday','Tuesday','Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        datasets: [{
            label: 'Temperature',
            borderColor: '#50509f',
            data: [weeklyChartD.temp.Monday,weeklyChartD.temp.Tuesday,weeklyChartD.temp.Wednesday,weeklyChartD.temp.Thursday,
                weeklyChartD.temp.Friday,weeklyChartD.temp.Saturday, weeklyChartD.temp.Sunday]
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    suggestedMin: 0,
                    suggestedMax: 35
                }
            }]
        }
    }
});

var phWeeklyChartid = document.getElementById('phWeeklyChart').getContext('2d');
var phWeeklyChart = new Chart(phWeeklyChartid, {
    type: 'bar',
    data: {
        labels: ['Monday','Tuesday','Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        datasets: [{
            label: 'pH',
            borderColor: '#50509f',
            data: [weeklyChartD.ph.Monday,weeklyChartD.ph.Tuesday,weeklyChartD.ph.Wednesday,weeklyChartD.ph.Thursday,
                weeklyChartD.ph.Friday,weeklyChartD.ph.Saturday, weeklyChartD.ph.Sunday]
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    suggestedMin: 0,
                    suggestedMax: 14
                }
            }]
        }
    }
});

var wfWeeklyChartid = document.getElementById('wfWeeklyChart').getContext('2d');
var wfWeeklyChart = new Chart(wfWeeklyChartid, {
    type: 'bar',
    data: {
        labels: ['Monday','Tuesday','Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        datasets: [{
            label: 'Filter Flow',
            borderColor: '#50509f',
            data: [weeklyChartD.flow.Monday,weeklyChartD.flow.Tuesday,weeklyChartD.flow.Wednesday,weeklyChartD.flow.Thursday,
                weeklyChartD.flow.Friday,weeklyChartD.flow.Saturday, weeklyChartD.flow.Sunday]
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    suggestedMin: 0,
                    suggestedMax: 100
                }
            }]
        }
    }
});

var clarityWeeklyChartid = document.getElementById('clarityWeeklyChart').getContext('2d');
var clarityWeeklyChart = new Chart(clarityWeeklyChartid, {
    type: 'bar',
    data: {
        labels: ['Monday','Tuesday','Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        datasets: [{
            label: 'Water Clarity',
            borderColor: '#50509f',
            data: [weeklyChartD.clarity.Monday,weeklyChartD.clarity.Tuesday,weeklyChartD.clarity.Wednesday,weeklyChartD.clarity.Thursday,
                weeklyChartD.clarity.Friday,weeklyChartD.clarity.Saturday, weeklyChartD.clarity.Sunday]
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    suggestedMin: 0,
                    suggestedMax: 10
                }
            }]
        }
    }
});

//
// Monthly average chart section
//
var tempMonthlyChartid = document.getElementById('temperatureMonthlyChart').getContext('2d');
var tempMonthlyChart = new Chart(tempMonthlyChartid, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: 'Temperature',
            borderColor: '#50509f',
            data: []
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    suggestedMin: 0,
                    suggestedMax: 35
                }
            }]
        }
    }
});

var phMonthlyChartid = document.getElementById('phMonthlyChart').getContext('2d');
var phMonthlyChart = new Chart(phMonthlyChartid, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: 'pH',
            borderColor: '#50509f',
            data: []
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    suggestedMin: 0,
                    suggestedMax: 14
                }
            }]
        }
    }
});

var wfMonthlyChartid = document.getElementById('wfMonthlyChart').getContext('2d');
var wfMonthlyChart = new Chart(wfMonthlyChartid, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: 'Waterflow',
            borderColor: '#50509f',
            data: []
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    suggestedMin: 0,
                    suggestedMax: 100
                }
            }]
        }
    }
});

var clarityMonthlyChartid = document.getElementById('clarityMonthlyChart').getContext('2d');
var clarityMonthlyChart = new Chart(clarityMonthlyChartid, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: 'Water Clarity',
            borderColor: '#50509f',
            data: []
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    suggestedMin: 0,
                    suggestedMax: 10
                }
            }]
        }
    }
});

for (i=1; i < 32; i++) {
    if (monthlyChartD['temp'][i] || monthlyChartD['temp'][i] == 0) {
        console.log(monthlyChartD['temp'][i])
        addData(tempMonthlyChart, i.toString(), monthlyChartD['temp'][i])
        addData(phMonthlyChart, i.toString(), monthlyChartD['ph'][i])
        addData(wfMonthlyChart, i.toString(), monthlyChartD['flow'][i])
        addData(clarityMonthlyChart, i.toString(), monthlyChartD['clarity'][i])
    }
};

//
// Yearly average chart section
//
var tempYearlyChartid = document.getElementById('temperatureYearlyChart').getContext('2d');
var tempYearlyChart = new Chart(tempYearlyChartid, {
    type: 'bar',
    data: {
        labels: ['Jan','Feb','Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov','Dec'],
        datasets: [{
            label: 'Temperature',
            borderColor: '#50509f',
            data: [yearlyChartD.temp.January,yearlyChartD.temp.February,yearlyChartD.temp.March,yearlyChartD.temp.April,yearlyChartD.temp.May,
                yearlyChartD.temp.June,yearlyChartD.temp.July,yearlyChartD.temp.August,yearlyChartD.temp.September,yearlyChartD.temp.October,
                yearlyChartD.temp.November,yearlyChartD.temp.December]
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    suggestedMin: 0,
                    suggestedMax: 35
                }
            }]
        }
    }
});

var phYearlyChartid = document.getElementById('phYearlyChart').getContext('2d');
var phYearlyChart = new Chart(phYearlyChartid, {
    type: 'bar',
    data: {
        labels: ['Jan','Feb','Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov','Dec'],
        datasets: [{
            label: 'pH',
            borderColor: '#50509f',
            data: [yearlyChartD.ph.January,yearlyChartD.ph.February,yearlyChartD.ph.March,yearlyChartD.ph.April,yearlyChartD.ph.May,
                yearlyChartD.ph.June,yearlyChartD.ph.July,yearlyChartD.ph.August,yearlyChartD.ph.September,yearlyChartD.ph.October,
                yearlyChartD.ph.November,yearlyChartD.ph.December]
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    suggestedMin: 0,
                    suggestedMax: 14
                }
            }]
        }
    }
});

var wfYearlyChartid = document.getElementById('wfYearlyChart').getContext('2d');
var wfYearlyChart = new Chart(wfYearlyChartid, {
    type: 'bar',
    data: {
        labels: ['Jan','Feb','Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov','Dec'],
        datasets: [{
            label: 'Filter Flow',
            borderColor: '#50509f',
            data: [yearlyChartD.flow.January,yearlyChartD.flow.February,yearlyChartD.flow.March,yearlyChartD.flow.April,yearlyChartD.flow.May,
                yearlyChartD.flow.June,yearlyChartD.flow.July,yearlyChartD.flow.August,yearlyChartD.flow.September,yearlyChartD.flow.October,
                yearlyChartD.flow.November,yearlyChartD.flow.December]
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    suggestedMin: 0,
                    suggestedMax: 100
                }
            }]
        }
    }
});

var clarityYearlyChartid = document.getElementById('clarityYearlyChart').getContext('2d');
var clarityYearlyChartid = new Chart(clarityYearlyChartid, {
    type: 'bar',
    data: {
        labels: ['Jan','Feb','Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov','Dec'],
        datasets: [{
            label: 'Water Clarity',
            borderColor: '#50509f',
            data: [yearlyChartD.clarity.January,yearlyChartD.clarity.February,yearlyChartD.clarity.March,yearlyChartD.clarity.April,yearlyChartD.clarity.May,
                yearlyChartD.clarity.June,yearlyChartD.clarity.July,yearlyChartD.clarity.August,yearlyChartD.clarity.September,yearlyChartD.clarity.October,
                yearlyChartD.clarity.November,yearlyChartD.clarity.December]
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    suggestedMin: 0,
                    suggestedMax: 10
                }
            }]
        }
    }
});

//
// Functions for adding or removing data from charts
//
function addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        if (data) {
            dataset.data.push(data);
        } else {
            dataset.data.push(0);
        }
    });
    chart.update();
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
function changeTab(evt, tabName) {
    var i, x, tablinks;
    x = document.getElementsByClassName("dataSection");
    for (i = 0; i < x.length; i++) {
      x[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablink");
    console.log(tablinks)
    for (i = 0; i < x.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" w3-border-indigo", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.firstElementChild.className += " w3-border-indigo";
  }

