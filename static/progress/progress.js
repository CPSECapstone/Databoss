//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

app.controller('progress', function($scope, $location, $http) {
    console.log("on progress page");

    var captureName = $location.search()['name'];
    $http({
        method: 'GET',
        url: 'capture/' + captureName,
        headers: {
            'Content-Type': 'application/json'
        },
    }).then(function successCallback(response) {
        $scope.capture = response.data;
        calculateProgressCapture($scope.capture);
    }, function errorCallback(response) {
        console.log('error retrieving capture name = ' + captureName);
    });

    $scope.endCapture = function () {
        $http({
            method: 'POST',
            url: 'capture/endCapture',
            headers: {
                'Content-Type': 'application/json'
            },
            data: $scope.capture
        }).then(function successCallback(response) {
            console.log('success');

            $location.path('/metrics');
        }, function errorCallback(response) {
            console.log('error retrieving replays');
        });
    }
});

var calculateProgressCapture = function(capture) {
  console.log("HERE CALCULATING PROGRESS in progress page");
    var startTime = new Date(capture.startTime);
    startTime.setHours(startTime.getHours() + 8);
    var endTime = new Date(capture.endTime);
    endTime.setHours(endTime.getHours() + 8);
    var totalTimeMS = endTime - startTime;
    var currentTime = new Date(endTime);
    currentTime.setHours(currentTime.getHours() - 1);
    var elapsedTimeMS = currentTime - startTime;
    var percentage = (elapsedTimeMS/totalTimeMS) * 100;
    capture.progress = percentage.toFixed(0) + "%";
    console.log("capture progress: "  + capture.progress);
  }
