//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

app.controller('progress', function($scope, $location, $http) {

  var options = {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  };
  var captureName = $location.search()['name'];
  $http({
    method: 'GET',
    url: 'capture/' + captureName,
    headers: {
      'Content-Type': 'application/json'
    },
  }).then(function successCallback(response) {
    $scope.capture = response.data;
    if ($scope.capture.status !== "scheduled") {
      calculateProgressCapture($scope.capture);
    }
    else {
      var startTime = new Date($scope.capture.startTime);
      startTime.setHours(startTime.getHours() + 8);
      $scope.capture.progress = "Scheduled to start at " + startTime.toLocaleDateString('en-US', options);
      console.log($scope.capture.progress);
    }
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
  var startTime = new Date(capture.startTime);
  startTime.setHours(startTime.getHours() + 8);
  var endTime = new Date(capture.endTime);
  endTime.setHours(endTime.getHours() + 8);
  var totalTimeMS = endTime - startTime;
  var currentTime = Date.now();
  var elapsedTimeMS = currentTime - startTime;
  var percentage = (elapsedTimeMS/totalTimeMS) * 100;
  capture.progress = percentage.toFixed(0) + "%";
}
