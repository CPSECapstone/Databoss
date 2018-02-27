//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

app.controller('home', function($scope, $location, $http) {
        console.log("I'm home")
    $scope.goCapture = function () {
        console.log("HERE")
        $location.path('/capture');
    }
   $('.datepicker').datepicker();

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
        console.log('success');
    }, function errorCallback(response) {
        console.log('error retrieving captures');
    })
};
