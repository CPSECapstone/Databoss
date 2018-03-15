// Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

app.controller('progress', function($scope, $location, $http) {
  $scope.startDate = null;
  $scope.startTime = null;
  $scope.endDate = null;
  $scope.endTime = null;


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
    // prettyParseDate($scope.capture);
    if ($scope.capture.status !== "scheduled") {
      calculateProgressCapture($scope.capture, $location);
    }
    else {
      var startTime = new Date($scope.capture.startTime);
      startTime.setHours(startTime.getHours() + 7);
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
  };

  var progressInterval = setInterval(frame, 1000);
  function frame() {
    if (parseInt($scope.capture.progress.split("$")[0]) >= 100) {
      clearInterval(progressInterval);
      $scope.$apply(function() {
        $location.path('/metrics');
      });
    } else {
      $scope.$apply(function() {
        if ($scope.capture.status !== "scheduled") {
          calculateProgressCapture($scope.capture, $location);
        }
        else {
          var startTime = new Date($scope.capture.startTime);
          startTime.setHours(startTime.getHours() + 7);
          $scope.capture.progress = "Scheduled to start at " + startTime.toLocaleDateString('en-US', options);
          console.log($scope.capture.progress);
        }
      });
    }
  }

  $scope.$on('$locationChangeStart', function (event) {
    clearInterval(progressInterval);
  });

  $scope.displayMode = function(mode) {
    var result;
    if (mode === "time") result = "time-constrained";
    else if (mode === "storage") result = "storage";
    else if (mode === "interactive") result = "interactive";
    else result = mode;
    return result;
  };

  $scope.displayDate = function(date) {
    var date = new Date(date);
    var convertedDate = date.toLocaleString('en-US', {timeZone: 'UTC'});
    var dateTimeArray = convertedDate.split(", ");
    return dateTimeArray[0];
  };

  $scope.displayTime = function(date) {
    var date = new Date(date);
    var convertedDate = date.toLocaleString('en-US', {timeZone: 'UTC'});
    var dateTimeArray = convertedDate.split(", ");
    return dateTimeArray[1];
  }
});

var calculateProgressCapture = function(capture, $location) {
  var startTime = new Date(capture.startTime);
  startTime.setHours(startTime.getHours() + 7);
  var endTime = new Date(capture.endTime);
  endTime.setHours(endTime.getHours() + 7);
  var totalTimeMS = endTime - startTime;
  var currentTime = Date.now();
  var elapsedTimeMS = currentTime - startTime;
  var percentage = (elapsedTimeMS/totalTimeMS) * 100;
  capture.progress = percentage.toFixed(0) + "%";
}
