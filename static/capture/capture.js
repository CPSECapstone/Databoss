var app = angular.module('MyCRT');

app.controller('capture', function($scope, $location) {

    $scope.newCapture = function() {
        console.log("going to add new capture");
    };
});