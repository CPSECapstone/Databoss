//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

app.controller('home', function($scope, $location) {

    $scope.goCapture = function () {
        console.log("HERE")
        $location.path('/capture');
    }

});