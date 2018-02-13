//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

//app.controller('capture', ['$scope', '$location', '$modal', function($scope, $location, $modal) {
app.controller('capture', function ($scope, $location, $uibModal, $http) {
    console.log("in capture");
    $scope.open = function () {
        console.log('opening pop up');
        var modalInstance = $uibModal.open({
            templateUrl: '/static/capture/addDatabaseModal.html',
            controller: function ($scope, $uibModalInstance) {
                $scope.add = function () {
                    $http({
                        method: 'POST',
                        url: '/dbc/add',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        data: {
                            'name': $scope.name,
                            'host': $scope.host,
                            'port': $scope.port,
                            'username': $scope.username,
                            'password': $scope.password,
                            'database': $scope.database
                        }
                    }).then(function successCallback(response) {
                        console.log('success');
                    }, function errorCallback(response) {
                        console.log('error');
                    });

                    $uibModalInstance.close();
                };

                $scope.cancel = function () {
                    $uibModalInstance.dismiss('cancel');
                };
            }
        });

        modalInstance.result.then(function() {
            console.log("do we get here?")
            $scope.getDBConnections();
        });
    };

    $scope.getDBConnections = function() {
        console.log("getting db connections");

        $http({
            method: 'GET',
            url: 'capture/listDBinstances',
            headers: {
                'Content-Type': 'application/json'
            },
        }).then(function successCallback(response) {
            $scope.DBConnections = response.data;
            console.log('success');
        }, function errorCallback(response) {
            console.log('error');
        });
    };

    $scope.getDBConnections();

    var getBuckets = function() {
        $http({
            method: 'GET',
            url: 'capture/listbuckets',
            headers: {
                'Content-Type': 'application/json'
            },
        }).then(function successCallback(response) {
            $scope.buckets = response.data;
            console.log('success');
        }, function errorCallback(response) {
            console.log('error');
        });
    };

    getBuckets();

    $scope.startCapture = function () {
        $http({
            method: 'POST',

            url: 'capture/startCapture',
            headers: {
                'Content-Type' : 'application/json'
            },
            data : {
                'captureBucket' : $('#crBucket').val(),
                'metricsBucket' : $('#metricsBucket').val(),
                'database' : $('#dbSelect').val(),
                'startTime' : $('#startTime').val(),
                'endTime' : $('#endTime').val(),
            }
        });
        // code to turn on DB logging goes here
        console.log("---- STARTING CAPTURE ----")
        $location.path('/progress');
    }
});
