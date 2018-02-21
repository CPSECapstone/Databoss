//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

//whenever an action occurs on the metrics page, the controller will handle it
app.controller('metrics', function($scope, $location, $http, Metrics) {
   Metrics.setCPUChart(createChart('cpuChart', 'CPU (Percent)', 'Time (seconds)'));
   Metrics.setReadIOChart(createChart('readIOChart', 'Read IO (count/second)', 'Time (seconds)'));

   getCaptures($http, $scope);
   getReplays($http, $scope);

   // Function that is called whenever a checkbox is checked or unchecked
   // Handles calling the appropriate functions for updating the charts
   $scope.updateSelection = function(type, name, id, value) {
      if (value === true) {
         getMetrics($http, Metrics, name, type, id);
      }
      else {
         console.log("remove from dataset");
      }
   };

   $scope.toggleReplays = function(captureId) {
      $('.collapse' + captureId).toggle();
   };
});

var addMetricsToChart = function(chart, label, data, time) {
   if (chart.data.labels.length <= 0)
      chart.data.labels = time;

   chart.data.datasets.push({
      data: data,
      label: label,
      borderColor: 'rgba(10, 148, 255, 1)',
      fill: false
   });
   chart.update();
};

// TODO remove dataset from a chart; if last dataset, remove time labels too
var removeMetricsFromChart = function() {

};

// Function to execute an HTTP request to get CPU Metrics
var getMetrics = function($http, Metrics, name, type, id) {
    $http({
        method: 'GET',
        url: '/metrics/getMetrics?type=' + type + '&id=' + id,
        nheaders: {
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

        addMetricsToChart(Metrics.getCPUChart(), name, cpu, time);
        addMetricsToChart(Metrics.getReadIOChart(), name, readIO, time);
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
                    gridLines: {
                      color: "#585858"
                    },
                    scaleLabel: {
                        display: true,
                        labelString: yAxesLabel,
                        fontColor: "#D9D9D9"
                    },
                    ticks: {
                      fontColor: "#D9D9D9"
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: xAxesLabel,
                        fontColor: "#D9D9D9"
                    },
                    ticks: {
                      fontColor: "#D9D9D9"
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