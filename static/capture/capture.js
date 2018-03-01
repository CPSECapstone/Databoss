//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

//app.controller('capture', ['$scope', '$location', '$modal', function($scope, $location, $modal) {
app.controller('capture', function ($scope, $location, $uibModal, $http) {

    // setting variables
    const captureModeBar = document.getElementById('capture-mode-bar');
    const dateContainer = $('#date-container');
    const timeContainer = $('#time-container');
    const storageContainer = $('#storage-container');
    var selectedMode = "";


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
      selectedMode = $("input[name=mode]:checked").attr('id');
      // Updating view based on selected mode
      if (selectedMode === "capture-int") {
        hideButtons(dateContainer, timeContainer, storageContainer);
      }
      else if (selectedMode === "capture-time") {
        showButtons(dateContainer, timeContainer);
        hideButtons(storageContainer);
      }
      else if (selectedMode === "capture-storage") {
        hideButtons(dateContainer, timeContainer);
        showButtons(storageContainer);
      }
      else {
        console.error("NO MODE SELECTED");
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

                // 'storageLimit' : $('#')
                //unsure how to grab the value of the storage limit.
            }
        });

        // code to turn on DB logging goes here
        $location.path('progress').search({
          name : $('#captureName').val()});
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
