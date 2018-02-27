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