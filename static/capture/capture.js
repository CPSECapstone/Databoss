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
    $scope.disabled = true;

    //setup
    buttonDisplay.hideButtons(dateContainer, timeContainer, storageContainer);

    $('input[name=mode]').on('change', function(event) {
      selectedMode = $("input[name=mode]:checked").val();
      console.log("value " + selectedMode);
      if (selectedMode === "interactive") {
        console.log("updating to interactive view");
        buttonDisplay.hideButtons(dateContainer, timeContainer, storageContainer);

        //VALIDATION LOGIC
        if ($('#captureName').val() && $('#crBucket').val()
            && $('#metricsBucket').val() && $('#dbName').val()) {
            $scope.$apply(function() {
                $scope.disabled = false;

            });
        }
        else {
            console.log("DISABLING THE BUTTON");
            $scope.$apply(function() {
                $scope.disabled = true;
            });
        }

      }
      else if (selectedMode === "time") {
        console.log("updating to time constrained view");
        buttonDisplay.showButtons(dateContainer, timeContainer);
        buttonDisplay.hideButtons(storageContainer);

        //VALIDATION LOGIC
        if ($('#startDate').val() == '' || $('#endDate').val() == '' ||
            $('#startTime').val() == '' || $('#endTime').val() == '') {
            $scope.$apply(function() {
                $scope.disabled = true;
            });

        }
        else {
            $scope.$apply(function() {
                $scope.disabled = false;
            });
        }

      }
      else if (selectedMode === "storage") {
        console.log("updating to storage view");
        buttonDisplay.hideButtons(dateContainer, timeContainer);
        buttonDisplay.showButtons(storageContainer);

        //VALIDATION LOGIC
        if ($('#storageNum').val() == '') {
            $scope.$apply(function() {
                $scope.disabled = true;
            });
        }
        else {
            $scope.$apply(function() {
                $scope.disabled = false;
            });
        }

      }
      else {
        console.log("NO MODE SELECTED");
      }
    });
    $scope.validateTime = function() {
        if ($('#startDate').val() == '' || $('#endDate').val() == '' ||
            $('#startTime').val() == '' || $('#endTime').val() == '') {
            return true;
        }
        if ($('#startDate').val() == $('#endDate').val() &&
            $('#startTime').val() >= $('#endTime').val()) {
            return true;
        }

        else {
            return false;
            console.log("returning false in time");
        }
    }

    $scope.validateStorage = function() {
        if ($('#storageNum').val() == '') {
            return true;
        }

        else {
            console.log("returning false in storage");
            return false;
        }
    }

    $scope.disableCaptureButton = function() {
        selectedMode = $("input[name=mode]:checked").val();
        if ($('#captureName').val() && $('#crBucket').val()
            && $('#metricsBucket').val() && $('#dbName').val()) {
            if (selectedMode === "time") {
                return validateTime();
            }
            else if (selectedMode === "storage") {
                return validateStorage();
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

    //returns true if capture button should be disabled
    //returns false if capture button should be enabled
    //for some reason it's like the modes are one behind everytime.
    //TRY PULLING THE VALUE OF THE MODE IN A DIFFERENT WAY POSSIBLY?
    $scope.disableCaptureButton = function() {
        console.log("IN DISABLE FUNCTION");

        disable = false;
        captureName = $('#captureName').val();
        captureBucket = $('#crBucket').val();
        metricsBucket = $('#metricsBucket').val();
        rdsInstance = $('#rdsInstance').val();
        dbName = $('#dbName').val();
        mode = $('input[name=mode]:checked').val();


        console.log("the mode is: " + mode);

        if (!captureName || !captureBucket || !metricsBucket || !rdsInstance) {
            console.log("should be here everytime");
            disabled = true;
        }

        if (mode == 'time') {
            startDate = $('#startDate').val();
            endDate = $('#endDate').val();
            startTime = $('#startTime').val();
            endTime = $('#endTime').val();

            if (!startDate || !endDate || !startTime || !endTime) {
                disable = true;
            }
        }
        if (mode == 'storage') {
            storageNum = $('#storageNum').val();

            if (!storageNum) {
                disable = true;
            }
        }

        return disable;

    };
});
