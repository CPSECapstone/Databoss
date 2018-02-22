//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

app.controller('progress', function($scope, $location, $http) {
    console.log("on progress page");

    var captureId = $location.search()['id'];
    $http({
        method: 'GET',
        url: 'capture/' + captureId,
        headers: {
            'Content-Type': 'application/json'
        },
    }).then(function successCallback(response) {
        $scope.capture = response.data;
    }, function errorCallback(response) {
        console.log('error retrieving capture id = ' + captureId);
    });

    $scope.endCapture = function () {
      // Code to end capture goes here - ng click is set up
      console.log("---- Ending Capture ----")
      $location.path('/metrics');
    }
});