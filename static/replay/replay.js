//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

app.controller('replay', function($scope, $http, $location) {
    console.log("in replay");

    $scope.startReplay = function () {
      // Add code to turn on DB logging here
      console.log("starting Replay!")
      $location.path('/progress');
    }

});
