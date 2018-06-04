// Module for managing the line colors for charts
var ChartColors = (function() {
    // array of colors to use for the metrics charts
    var colors = [
        'cornflowerblue',
        'tomato',
        'palegreen',
        'pink',
        'orange',
        'lemonchiffon',
        'aqua',
        'darkorchid',
        'lime',
        'red',
        'yellow',
        'violet'
    ];
    // array to keep track of used colors so line colors are unique
    var usedColors = [];

    return {
        getNextColor : function() {
            var availableColors = colors.filter(function(obj) { return usedColors.indexOf(obj) == -1; });
            usedColors.push(availableColors[0]);
            return availableColors[0];
        },
        removeUsedColor : function(color) {
            var index = usedColors.indexOf(color);
            if (index > -1) {
                usedColors.splice(index, 1);
            }
        },
        resetUsedColors : function() {
            usedColors = [];
        }
    };
})();

var cpuChart;
var readIOChart;
var writeIOChart;
var memoryChart;

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
app.controller('metrics', function($scope, $location, $http) {
    // Destroy any existing charts before creating new ones
    Chart.helpers.each(Chart.instances, function(instance) {
       instance.destroy();
    });

   ChartColors.resetUsedColors();

   cpuChart = createChart('cpuChart', 'CPU (Percent)', 'Time (seconds)');
   readIOChart = createChart('readIOChart', 'Read IO (count/second)', 'Time (seconds)');
   writeIOChart = createChart('writeIOChart', 'Write IO (count/second)', 'Time (seconds)');
   memoryChart = createChart('memoryChart', 'Memory (bytes)', 'Time (seconds)');

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
         getMetrics($http, name, type, id);
      else
        removeMetricsFromCharts(name);
   };

   $scope.toggleReplays = function(captureId, event) {
      if (event.target.classList.value == 'fa fa-caret-right') {
        event.target.classList.replace('fa-caret-right', 'fa-caret-down');
      }
      else {
        event.target.classList.replace('fa-caret-down', 'fa-caret-right');
      }

      $('.collapse' + captureId).toggle();
   };

   $scope.downloadLogFile = function(capture) {
       $http({
            method: 'GET',
            url: 'metrics/getLogfileObj',
            headers: {
                'Content-Type': 'application/json'
            },
            params : {'logfileId' : capture.logfileId}
        }).then(function successCallback(response) {
            logfileObj = response.data;
            var filenameOneSpace = (logfileObj.filename).replace(" ", "+");
            var filenameNoSpace = filenameOneSpace.replace(" ", "+");
            window.open('https://s3-us-west-1.amazonaws.com/' + logfileObj.bucket + '/' + filenameNoSpace, '_blank');

        }, function errorCallback(response) {
            console.log('Error in retrieving capture bucket from capture name');
        });
   };

   $scope.downloadMetricFile = function(capture) {
    $http({
        method: 'GET',
        url: 'metrics/getMetricFileObj',
        headers: {
            'Content-Type': 'application/json'
        },
        params : {'metricId' : capture.metricId}
    }).then(function successCallback(response) {
        metricFileObj = response.data;
        console.log(metricFileObj);
        var filenameOneSpace = (metricFileObj.filename).replace(" ", "+");
        var filenameNoSpace = filenameOneSpace.replace(" ", "+");
        window.open('https://s3-us-west-1.amazonaws.com/' + metricFileObj.bucket + '/' + filenameNoSpace, '_blank');

    }, function errorCallback(response) {
        console.log('Error in retrieving capture bucket from capture name');
    });
   };



  $scope.showInfo = function(item) {
    console.log(" i was clicked!!! ");
    if (item) {
      $scope.itemName = item.name;
      $scope.infoItem = item;
      $('#informationMetricsModal').modal('show');
    }
  }

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
var removeMetricsFromCharts = function(name) {
    var color;

    Chart.helpers.each(Chart.instances, function(instance) {
        var datasets = instance.chart.config.data.datasets;

        for (index = 0; index < datasets.length; index++)
            if (datasets[index].label === name)
                break;

        // Set the color for the dataset to be available
        if (!color) {
            color = datasets[index].borderColor;
            ChartColors.removeUsedColor(color);
        }

        datasets.splice(index, 1);
        instance.update();
    });

    updateAllChartTimes();
};

// Updates the time labels for every chart to be consistent with the datasets
var updateAllChartTimes = function() {
    var time = [];
    var datasets = cpuChart.data.datasets;

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

// Function to execute an HTTP request to get Metrics
var getMetrics = function($http, name, type, id) {
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

        var color = ChartColors.getNextColor();

        addMetricsToChart(cpuChart, name, cpu, cpuTime, color);
        addMetricsToChart(readIOChart, name, readIO, readIOTime, color);
        addMetricsToChart(writeIOChart, name, writeIO, writeIOTime, color);
        addMetricsToChart(memoryChart, name, memory, memoryTime, color);
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
                      fontColor: "#D9D9D9",
                      maxTicksLimit: 30
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
        url: 'capture/getCapturesWithBuckets',
        headers: {
        'Content-Type': 'application/json'
        },
    }).then(function successCallback(response) {
        $scope.captures = response.data;
        $scope.captures.map(capture => {
          capture.type = "capture";
        });
        formatDates($scope.captures);
//        $scope.captures = response.data.filter(capture =>
//            capture.status == "finished");

    }, function errorCallback(response) {
        console.log('error retrieving captures');
    })
};

//Makes an HTTP GET Request to retrieve a list of the replays
var getReplays = function($http, $scope) {
    $http({
        method: 'GET',
        url: 'replay/getReplaysWithBuckets',
        headers: {
        'Content-Type': 'application/json'
        },
    }).then(function successCallback(response) {
        $scope.replays = response.data;
        $scope.replays.map(replay => {
          replay.type = "replay";
        });
        console.log($scope.replays[0]);
        formatDates($scope.replays);
    }, function errorCallback(response) {
        console.log('error retrieving replays');
    })
};
