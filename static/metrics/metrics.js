//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

//whenever an action occurs on the metrics page, the controller will handle it
app.controller('metrics', function($scope, $location, $http, Metrics) {
   Metrics.setCPUChart(createChart('cpuChart', 'CPU (Percent)', 'Time (seconds)'));
   Metrics.setReadIOChart(createChart('readIOChart', 'Read IO (count/second)', 'Time (seconds)'));

   //    $scope.captures = [{"Id": 1, "name" : "Capture 1", "date" : "01/12/17"},
   //                        {"Id": 2, "name" : "Capture 2", "date" : "01/12/17"}];
   //    $scope.replays = [{"Id" : 2, "name" : "Replay 1", "date" : "01/12/17", "captureId" : 1},
   //                      {"Id" : 3, "name" : "Replay 2", "date" : "01/12/17", "captureId" : 2}];

   getCaptures($http, $scope);
   getReplays($http, $scope);
//   getMetrics($http, Metrics);

   $scope.updateSelection = function(type, id, value) {
      if (value === true) {
         getMetrics($http, Metrics, type, id);
      }
      else {
         console.log("remove from dataset");
      }
   };
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
var getMetrics = function($http, Metrics, type, id) {
    $http({
        method: 'GET',
        url: '/metrics/getMetrics?type=' + type + '&id=' + id,
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

var getCaptures = function($http, $scope) {
    $http({
        method: 'GET',
        url: 'capture/getAll',
        headers: {
        'Content-Type': 'application/json'
        },
    }).then(function successCallback(response) {
        $scope.captures = response.data;
        console.log('success');
    }, function errorCallback(response) {
        console.log('error retrieving captures');
    })
};

//Makes an HTTP GET Request to retrieve a list of the replays
var getReplays = function($http, $scope) {
    $http({
        method: 'GET',
        url: 'replay/getAll',
        headers: {
        'Content-Type': 'application/json'
        },
    }).then(function successCallback(response) {
        $scope.replays = response.data;
        console.log('success');
    }, function errorCallback(response) {
        console.log('error retrieving replays');
    })
};