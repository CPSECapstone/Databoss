//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

app.controller('login', function($scope, $location, $http) {
    $scope.login = function() {
        $http({
            method: 'POST',
            url: '/login/aws',
            headers: {
                'Content-Type': 'application/json'
            },
            data: {
                'access_key': $scope.accessKey,
                'secret_key': $scope.secretKey
            }
        }).then(function successCallback(response) {
            console.log('success');
            $location.path('/home');
        }, function errorCallback(response) {
            console.log('error');
        });
    }

});