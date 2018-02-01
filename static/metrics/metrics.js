//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

//whenever an action occurs on the metrics page, the controller will handle it
app.controller('metrics', function($scope, $location, $http) {
    getCPUMetrics($http);
    $scope.workloads = [{ "name":"Capture 1", "date":"01/12/17" }];
    //$scope.workloads = getWorkloads();
});

// Function to execute an HTTP request to get CPU Metrics
var getCPUMetrics = function($http) {
    $http({
        method: 'GET',
        url: '/metrics/getCPU',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function successCallback(response) {
        console.log('success');
        var cpu = response.data.cpu;
        var time = response.data.cpuTime;
        var baseTime = time[0];

        // start the time at 0 seconds
        time = time.map(function(value) {
            return value - baseTime;
        });

        createChart(time, cpu, "CPU");
    }, function errorCallback(response) {
        console.log('error');
    });
};

var createChart = function(labels, data, label) {
    var ctx = document.getElementById("myChart");
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                label: label,
                borderColor: 'rgba(10, 148, 255, 1)',
                backgroundColor:'rgba(10, 148, 255, 0.57)'
            }]
        },
        options : {
          scales: {
            yAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'CPU (Percent)'
              }
            }],
            xAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'Time (seconds)'
              }
            }]
          }
        }
    });
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