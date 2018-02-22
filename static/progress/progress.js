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
    }, function errorCallback(response) {
        console.log('error retrieving capture name = ' + captureName);
    });

    $scope.endCapture = function () {
      // Code to end capture goes here - ng click is set up
      console.log("---- Ending Capture ----")
      $location.path('/metrics');
    }
});