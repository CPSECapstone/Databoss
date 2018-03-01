//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT').directive('onFinishRender', function ($timeout) {
    return {
        restrict: 'A',
        link: function (scope, element, attr) {
            if (scope.$last === true) {
                $timeout(function () {
                    scope.$emit(attr.onFinishRender);
                });
            }
        }
    }
});

//whenever an action occurs on the metrics page, the controller will handle it
app.controller('metrics', function($scope, $location, $http, Metrics) {
   Metrics.setCPUChart(createChart('cpuChart', 'CPU (Percent)', 'Time (seconds)'));
   Metrics.setReadIOChart(createChart('readIOChart', 'Read IO (count/second)', 'Time (seconds)'));
   Metrics.setWriteIOChart(createChart('writeIOChart', 'Write IO (count/second)', 'Time (seconds)'));
   Metrics.setMemoryChart(createChart('memoryChart', 'Memory (bytes)', 'Time (seconds)'));

   getCaptures($http, $scope);
   getReplays($http, $scope);

   $scope.$on('updateSelectionFromQueryParameters', function(ngRepeatFinishedEvent) {
     var captureId = $location.search()['captureId'];

     if (captureId) {
       $('#capture-checkbox' + captureId).click();
     }
  });

   // Function that is called whenever a checkbox is checked or unchecked
   // Handles calling the appropriate functions for updating the charts
   $scope.updateSelection = function(type, name, id, value) {
      if (value === true)
         getMetrics($http, Metrics, name, type, id);
      else
        removeMetricsFromCharts(Metrics, name);
   };

   $scope.toggleReplays = function(captureId) {
      $('.collapse' + captureId).toggle();
   };
});

var addMetricsToChart = function(chart, label, data, time, color) {
   chart.data.datasets.push({
      data: data,
      label: label,
      borderColor: color,
      fill: false,
      time: time
   });
   updateAllChartTimes();
};

// Removes a specific metrics dataset from all the metrics charts
var removeMetricsFromCharts = function(Metrics, name) {
    var color;

    Chart.helpers.each(Chart.instances, function(instance) {
        var datasets = instance.chart.config.data.datasets;

        for (index = 0; index < datasets.length; index++)
            if (datasets[index].label === name)
                break;

        // Set the color for the dataset to be available
        if (!color) {
            color = datasets[index].borderColor;
            console.log(color);
            Metrics.removeUsedColor(color);
        }

        datasets.splice(index, 1);
        instance.update();
    });

    updateAllChartTimes();
};

// Updates the time labels for every chart to be consistent with the datasets
var updateAllChartTimes = function() {
    var time = [];
    var datasets = Chart.instances[0].chart.config.data.datasets;

    // Combine the times for each dataset and keep only the unique values
    datasets.forEach(function(dataset) {
        time = time.concat(dataset.time);
    });
    time = Array.from(new Set(time));

    // Set the time labels for each chart to the updated times
    Chart.helpers.each(Chart.instances, function(instance) {
        instance.chart.config.data.labels = time;
        instance.update();
    });
};

// Convert the array of epoch times to start at 0 seconds for comparing metrics
// regardless of start datetime
var convertTimeArrayFromEpoch = function(times) {
    var baseTime = times[0];

    relativeTimes = times.map(function(value) {
        return value - baseTime;
    });

    return relativeTimes;
}

// Function to execute an HTTP request to get CPU Metrics
var getMetrics = function($http, Metrics, name, type, id) {
    $http({
        method: 'GET',
        url: '/metrics/getMetrics?type=' + type + '&id=' + id,
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function successCallback(response) {
        console.log('success');
        var cpu = response.data.cpu;
        var cpuTime = convertTimeArrayFromEpoch(response.data.cpuTime);
        var readIO = response.data.readIO;
        var readIOTime = convertTimeArrayFromEpoch(response.data.readIOTime);
        var writeIO = response.data.writeIO;
        var writeIOTime = convertTimeArrayFromEpoch(response.data.writeIOTime);
        var memory = response.data.memory;
        var memoryTime = convertTimeArrayFromEpoch(response.data.memoryTime);

        var color = Metrics.getNextColor();

        addMetricsToChart(Metrics.getCPUChart(), name, cpu, cpuTime, color);
        addMetricsToChart(Metrics.getReadIOChart(), name, readIO, readIOTime, color);
        addMetricsToChart(Metrics.getWriteIOChart(), name, writeIO, writeIOTime, color);
        addMetricsToChart(Metrics.getMemoryChart(), name, memory, memoryTime, color);
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
            legend: {
                display: true,
                labels: {
                    fontColor: "#D9D9D9"
                }
            },
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
