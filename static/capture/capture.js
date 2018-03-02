//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

//app.controller('capture', ['$scope', '$location', '$modal', function($scope, $location, $modal) {
app.controller('capture', function ($scope, $location, $uibModal, $http) {
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
                'captureName' : $('#captureName').val(),
                'captureBucket' : $('#crBucket').val(),
                'metricsBucket' : $('#metricsBucket').val(),
                'dbName' : $('#dbName').val(),
                'startDate' : $('#startDate').val(),
                'endDate' : $('#endDate').val(),
                'startTime' : $('#startTime').val(),
                'endTime' : $('#endTime').val(),
                'mode' : $('input[name=mode]:checked').val()
            }
        });
        if ($('input[name=mode]:checked').val() == 'time') {
            $location.path('home'); 
        }
        else {
            $location.path('progress').search({name : $('#captureName').val()});
        }
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
