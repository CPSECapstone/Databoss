//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

app.controller('home', function($scope, $location, $http) {
    $scope.goCapture = function () {
        $location.path('/capture');
    }

    populateCaptures($http, $scope);

});

var populateCaptures = function($http, $scope) {
    $http({
        method: 'GET',
        url: 'capture/getAll',
        headers: {
        'Content-Type': 'application/json'
        },
    }).then(function successCallback(response) {
        $scope.captures = response.data;
        calculateProgress($scope.captures);
        console.log('success');
    }, function errorCallback(response) {
        console.log('error retrieving captures');
    })
};

var calculateProgress = function(captures) {
  console.log("HERE CALCULATING PROGRESS");
  var totalTimeMS = null;
  var startTime = null;
  var endTime = null;
  var elapsedTimeMS = null;
  var currentTime = null;
  var percentage = null;
  for (var i = 0; i < captures.length; i++) {
    startTime = new Date(captures[i].startTime);
    startTime.setHours(startTime.getHours() + 8);
    endTime = new Date(captures[i].endTime);
    endTime.setHours(endTime.getHours() + 8);
    totalTimeMS = endTime - startTime;
    currentTime = new Date(endTime);
    currentTime.setHours(currentTime.getHours() - 1);
    elapsedTimeMS = currentTime - startTime;
    percentage = (elapsedTimeMS/totalTimeMS) * 100;
    captures[i].progress = percentage.toFixed(0) + "%";
    console.log("progress: "  + captures[i].progress);
  }

}
