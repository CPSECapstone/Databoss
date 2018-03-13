//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

app.controller('capture', function ($scope, $location, $http) {
    console.log("in capture");

    // setting variables
    const captureModeBar = document.getElementById('capture-mode-bar');
    const dateContainer = $('#date-container');
    const timeContainer = $('#time-container');
    const storageContainer = $('#storage-container');
    var selectedMode = "";
    $scope.required = true;

    //setting an observer for the captureModeBar to change input view when clicked
    const hideButtons = function() {
      console.log(arguments);
      for (var i = 0; i < arguments.length; i++) {
        arguments[i].hide();
      }
    }

    const showButtons = function() {
      console.log(arguments);
      for (var i = 0; i < arguments.length; i++) {
        arguments[i].show();
      }
    }

    //setup
    hideButtons(dateContainer, timeContainer, storageContainer);

    $('input[name=mode]').on('change', function(event) {
      selectedMode = $("input[name=mode]:checked").val();
      console.log("value " + selectedMode);
      if (selectedMode === "interactive") {
        console.log("updating to interactive view");
        hideButtons(dateContainer, timeContainer, storageContainer);
      }
      else if (selectedMode === "time") {
        console.log("updating to time constrained view");
        showButtons(dateContainer, timeContainer);
        hideButtons(storageContainer);
      }
      else if (selectedMode === "storage") {
        console.log("updating to storage view");
        hideButtons(dateContainer, timeContainer);
        showButtons(storageContainer);
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
        if ($('#captureName').val() == '' || $('#crBucket').val() == null ||
            $('#metricsBucket').val() == null || $('#dbName').val() == null) {
            return;
        }
        if ($('input[name=mode]:checked').val() == 'time' &&
            ($('#startDate').val() == '' || $('#endDate').val() == '' ||
             $('#startTime').val() == '' || $('#endTime').val() == '' ||
             ($('#startDate').val() == $('#endDate').val() && $('#startTime').val() > $('#endTime').val()))) {
            return;
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
                'mode' : $('input[name=mode]:checked').val()
            }
        }).then(function successCallback(response) {
            if ($('input[name=mode]:checked').val() == 'time') {
                $location.path('home');
            }
            else {
                $location.path('progress').search({name : $('#captureName').val()});
            }
        }, function errorCallback(response) {
            console.log('Error POSTing capture object to database.');
        });
    }

    $scope.setStorageSize = function (id) {
      console.log(id);
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
});
