//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

app.controller('capture', function ($scope, $location, $http, buttonDisplay, activeNavItem) {
    // setting variables
    const captureModeBar = document.getElementById('capture-mode-bar');
    const dateContainer = $('#date-container');
    const timeContainer = $('#time-container');
    const storageContainer = $('#storage-container');
    var selectedMode = "";
    $scope.required = true;
    $scope.disabled = true;
    $scope.startBeforeCurrent = false;
    $scope.mode = "interactive";

    buttonDisplay.hideButtons(dateContainer, timeContainer, storageContainer);

    $('input[name=mode]').on('change', function(event) {
      selectedMode = $("input[name=mode]:checked").val();

      if (selectedMode === "interactive") {
        buttonDisplay.hideButtons(dateContainer, timeContainer, storageContainer);
        $scope.startBeforeCurrent = false;

        //Disable or enable capture button
        $scope.$apply(function() {
            $scope.disabled = $scope.validateInteractive();
        });
      }
      else if (selectedMode === "time") {
        buttonDisplay.showButtons(dateContainer, timeContainer);
        buttonDisplay.hideButtons(storageContainer);

        //Disable or enable capture button
        $scope.$apply(function() {
            $scope.disabled = $scope.validateTime();
        })
      }
      else if (selectedMode === "storage") {
        buttonDisplay.hideButtons(dateContainer, timeContainer);
        buttonDisplay.showButtons(storageContainer);
        $scope.startBeforeCurrent = false;

        //Disable or enable capture button
        $scope.$apply(function() {
            $scope.disabled = $scope.validateStorage();
        })
      }
    });

    $scope.validateInteractive = function() {
        console.log("validating interactive");
        if ($('#captureName').val() && $('#crBucket').val()
            && $('#metricsBucket').val() && $('#dbName').val()) {
            console.log("returning false");
            return false;
        }
        else {

            return true;
        }
    }

    $scope.validateTime = function() {
        if ($('#startDate').val() == '' || $('#endDate').val() == '' ||
            $('#startTime').val() == '' || $('#endTime').val() == '') {
            return true;
        }

        if (Date.parse($('#startDate').val() + ' ' + $('#startTime').val()) <= Date.now()) {
            $scope.startBeforeCurrent = true;
        }
        else { $scope.startBeforeCurrent = false; }

        if (Date.parse($('#startDate').val() + ' ' + $('#startTime').val()) >=
            Date.parse($('#endDate').val() + ' ' + $('#endTime').val()) ||
            Date.parse($('#endDate').val() + ' ' + $('#endTime').val()) <= Date.now()) {
            return true;
        }

        return false;
    }

    $scope.validateStorage = function() {
        if ($('#storageNum').val() == '') {
            return true;
        }

        else {
            return false;
        }
    }

    $scope.disableCaptureButton = function() {
        selectedMode = $("input[name=mode]:checked").val();
        if (!($scope.validateInteractive())) {
            if (selectedMode === "time") {
                return $scope.validateTime();
            }
            else if (selectedMode === "storage") {
                return $scope.validateStorage();
            }
        }
        else {
            return false;
        }
    }

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
                $('#authenticationModal').modal('hide');
                console.log('success');
            }, function errorCallback(response) {
                $scope.instanceDbs = 'false';
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

        var captureName = $('#captureName').val();
        captureName = captureName.trim();

        $http({
            method: 'POST',
            url: 'capture/startCapture',
            headers: {
                'Content-Type' : 'application/json'
            },
            data : {
                'captureName' : captureName,
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
            console.log("Successful response is: ", response.status);
            const inputMode = $('input[name=mode]:checked').val();
            if (inputMode == 'time' || inputMode == 'storage') {
                activeNavItem.clearAndMakeItemActive('homeTab');
                $location.path('home');

            }
            else {
                $location.path('progress').search({name : captureName});
            }
        },function errorCallback(response) {
            console.log("The response is: " + response.status);
            if (response.status === 400) {
                $scope.error = "There is not enough allocated storage in your the RDS instance.";
            }
            else if (response.status === 408) {
                $scope.error = "Invalid end time"
            }
            else {
                $scope.error = "Storage cannot be zero or negative";
            }


        });
    }

    $scope.setStorageSize = function (id) {
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
