//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

app.controller('progress', function($scope, $location, $http) {
    console.log("on progress page");

    $scope.endCapture = function () {
      // Code to end capture goes here - ng click is set up
      console.log("---- Ending Capture ----")
    }
});
