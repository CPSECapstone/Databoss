//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

//whenever an action occurs on the metrics page, the controller will handle it
app.controller('metrics', function($scope, $location, $http, Metrics) {
    Metrics.setCPUChart(createChart('cpuChart', 'CPU (Percent)', 'Time (seconds)'));
    Metrics.setReadIOChart(createChart('readIOChart', 'Read IO (count/second)', 'Time (seconds)'));

    $scope.workloads = [{ "name":"Capture 1", "date":"01/12/17" }];
    //$scope.workloads = getWorkloads();
    getMetrics($http, Metrics);
});

var workloadChecked = function() {
    // TODO get value from checked box and get its corresponding metrics file
};

var addMetricsToChart = function(chart, label, data, time) {
    chart.data.labels = time;
    chart.data.datasets.push({
        data: data,
        label: label,
        borderColor: 'rgba(10, 148, 255, 1)',
        fill: false
    });
    chart.update();
};

// Function to execute an HTTP request to get CPU Metrics
var getMetrics = function($http, Metrics) {
    $http({
        method: 'GET',
        url: '/metrics/getMetrics',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function successCallback(response) {
        console.log('success');
        var cpu = response.data.cpu;
        var time = response.data.cpuTime;
        var baseTime = time[0];
        var readIO = response.data.readIO;

        // start the time at 0 seconds
        time = time.map(function(value) {
            return value - baseTime;
        });

        // TODO change capture 1 to response.data.name or some equivalent
        addMetricsToChart(Metrics.getCPUChart(), 'Capture 1', cpu, time);
        addMetricsToChart(Metrics.getReadIOChart(), 'Capture 1', readIO, time);
    }, function errorCallback(response) {
        console.log('error');
    });
};

// Function that creates an empty line chart for a chart element having id=elementId
// with provided axes labels.
// Returns the newly created chart
var createChart = function(elementId, yAxesLabel, xAxesLabel) {
    var ctx = document.getElementById(elementId);
    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: []
        },
        options : {
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: yAxesLabel
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: xAxesLabel
                    }
                }]
            }
        }
    });
    return chart;
};

var getWorkloads = function($http) {
    $http({
        method: 'GET',
        url: 'workloads/listWorkloads',
        headers: {
        'Content-Type': 'application/json'
        },
    }).then(function successCallback(response) {
        $scope.workloads = response.data;
        console.log('success');
    }, function errorCallback(response) {
        console.log('error');
    })
};
