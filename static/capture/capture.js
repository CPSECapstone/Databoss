//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

app.controller('capture', function ($scope, $location, $http, buttonDisplay) {
    // setting variables
    const captureModeBar = document.getElementById('capture-mode-bar');
    const dateContainer = $('#date-container');
    const timeContainer = $('#time-container');
    const storageContainer = $('#storage-container');
    var selectedMode = "";
    $scope.error = "";
    $scope.required = true;

    //setup
    buttonDisplay.hideButtons(dateContainer, timeContainer, storageContainer);

    $('input[name=mode]').on('change', function(event) {
      selectedMode = $("input[name=mode]:checked").val();
      console.log("value " + selectedMode);
      if (selectedMode === "interactive") {
        console.log("updating to interactive view");
        buttonDisplay.hideButtons(dateContainer, timeContainer, storageContainer);
      }
      else if (selectedMode === "time") {
        console.log("updating to time constrained view");
        buttonDisplay.showButtons(dateContainer, timeContainer);
        buttonDisplay.hideButtons(storageContainer);
      }
      else if (selectedMode === "storage") {
        console.log("updating to storage view");
        buttonDisplay.hideButtons(dateContainer, timeContainer);
        buttonDisplay.showButtons(storageContainer);
      }
      else {
        console.log("NO MODE SELECTED");
      }
    });

    $scope.getRDSInstances = function() {
        console.log("getting db connections");

        $http({
            method: 'GET',
            url: 'capture/listDBinstances',
            headers: {
                'Content-Type': 'application/json'
            },
        }).then(function successCallback(response) {
            $scope.RDSInstances = response.data;
            console.log('success');
        }, function errorCallback(response) {
            console.log('error');
        });
    };

    $scope.getRDSInstances();

    $scope.authenticateInstance = function(instance) {
        if (instance) {
            $scope.currentRDSInstance = JSON.parse(instance).DBInstanceIdentifier;
            $('#authenticationModal').modal('show');
        }
    }

    $scope.getInstanceDbs = function(instance) {
        if (instance) {
            var endpoint = JSON.stringify(JSON.parse(instance).Endpoint);
            $http({
                method: 'POST',
                url: 'capture/listInstanceDbs/' + endpoint,
                headers: {
                    'Content-Type': 'application/json'
                },
                data: {
                    'username': $scope.username,
                    'password': $scope.password
                }
            }).then(function successCallback(response) {
                console.log(response.data);
                $scope.instanceDbs = response.data;
                console.log('success');
            }, function errorCallback(response) {
                console.log('error');
            });
        }
    };

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

    var captureNames = function () {
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
    }

    // Defaulted mode is interactive when no mode is chosen
    $scope.startCapture = function () {

        if (!$scope.storageType) {
            console.log("storage type undefined");
            $scope.storageType = "";
        }

        $http({
            method: 'POST',
            url: 'capture/startCapture',
            headers: {
                'Content-Type' : 'application/json'
            },
            data : {
                'captureName' : $('#captureName').val(),
                'captureBucket' : $('#crBucket').val(),
                'metricsBucket' : $('#metricsBucket').val(),
                'rdsInstance' : JSON.parse($('#rdsInstance').val()).DBInstanceIdentifier,
                'dbName': $('#dbName').val(),
                'username': $scope.username,
                'password': $scope.password,
                'startDate' : $('#startDate').val(),
                'endDate' : $('#endDate').val(),
                'startTime' : $('#startTime').val(),
                'endTime' : $('#endTime').val(),
                'storageNum' : $('#storageNum').val(),
                'storageType' : $scope.storageType,
                'mode' : $('input[name=mode]:checked').val()
            }
        }).then(function successCallback(response) {
            console.log(response);
            const inputMode = $('input[name=mode]:checked').val();
            if (inputMode == 'time' || inputMode == 'storage') {
                $location.path('home');
            }
            else {
                $location.path('progress').search({name : $('#captureName').val()});
            }
        }, function errorCallback(response) {
            $scope.error = "There is not enough allocated storage in your the RDS instance.";
        });
    }

    $scope.setStorageSize = function (id) {
      console.log(id);
      $scope.storageType = id;
      //clear active
      if (id === "mb-button") {
        document.getElementById(id).classList.add('active');
        document.getElementById('gb-button').classList.remove('active');

      }
      else {
        document.getElementById(id).classList.add('active');
        document.getElementById('mb-button').classList.remove('active');
      }
    }

    $scope.checkCaptureName = function(name) {
        $http({
            method: 'GET',
            url: 'capture/checkName?name=' + name,
            headers: {
                'Content-Type' : 'application/json'
            }
        }).then(function successCallback(response) {
            $scope.uniqueName = response.data;
        }, function errorCallback(response) {

        });
    };
});
