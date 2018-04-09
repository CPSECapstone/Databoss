//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

app.controller('replay', function($scope, $http, $location) {
    const dateContainer = $('#date-container');
    const timeContainer = $('#time-container');
    const storageContainer = $('#storage-container');

<<<<<<< HEAD
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

    hideButtons(dateContainer, timeContainer, storageContainer);

    $('input[name=mode]').on('change', function(event) {
      selectedMode = $("input[name=mode]:checked").attr('id');
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
        console.log("NO MODE SELECTED");
      }
    });

=======
>>>>>>> origin
    var today = new Date(new Date().getFullYear(), new Date().getMonth(), new Date().getDate());
    $('#startDate').datepicker({
      iconsLibrary: 'fontawesome',
      minDate: today,
      maxDate: function () {
        return $('#endDate').val();
      }
    });
    $('#endDate').datepicker({
      iconsLibrary: 'fontawesome',
      minDate: function () {
        return $('#startDate').val();
      }
    });
    $('#startTime').timepicker({
      iconsLibrary: 'fontawesome',
    });
    $('#endTime').timepicker({
      iconsLibrary: 'fontawesome',
    });

    $scope.startReplay = function () {
        $http({
                method: 'POST',
                url: 'replay/startReplay',
                headers: {
                    'Content-Type' : 'application/json'
                },
                data : {
                    'replayName' : $('#replayName').val(),
                    'capture' : $('#capture').val(),
                    'dbName' : $('#dbName').val(),
                    'username': $scope.username,
                    'password': $scope.password,
                    'startDate' : $('#startDate').val(),
                    'endDate' : $('#endDate').val(),
                    'startTime' : $('#startTime').val(),
                    'endTime' : $('#endTime').val(),
                    'replayMode' : $('input[name=replayMode]:checked').val()
                }
            });
      // Add code to turn on DB logging here
      console.log("Starting Replay!")
      // @TODO Need to fix the reroute to the started replay.
      $location.path('/home');

    }

    $scope.setStorageSize = function (id) {
      //clear active
      if (id === "mb-button") {
        document.getElementById(id).classList.add('active');
        document.getElementById('gb-button').classList.remove('active');
      }
      else {
        document.getElementById('gb-button').classList.add('active');
        document.getElementById('mb-button').classList.remove('active');
      }
    }

    populateCaptures($http, $scope);
//    getDBConnections($http, $scope);

    $scope.authenticateInstance = function(instance) {
        if (instance) {
            $scope.currentRDSInstance = JSON.parse(instance).DBInstanceIdentifier;
            $('#authenticationModal').modal('show');
        }
    };

    $scope.getRDSInstances = function() {
        $http({
            method: 'GET',
            url: 'capture/listDBinstances',
            headers: {
                'Content-Type': 'application/json'
            },
        }).then(function successCallback(response) {
            $scope.RDSInstances = response.data;
        }, function errorCallback(response) {
            console.log('error');
        });
    };

    $scope.getRDSInstances();

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
            }, function errorCallback(response) {
                console.log('error');
            });
        }
    };

    $scope.checkReplayName = function(name) {
        $http({
            method: 'GET',
            url: 'replay/checkName?name=' + name,
            headers: {
                'Content-Type' : 'application/json'
            }
        }).then(function successCallback(response) {
            $scope.uniqueName = response.data;
        }, function errorCallback(response) {

        });
    };
});

var populateCaptures = function($http, $scope) {
    $http({
        method: 'GET',
        url: 'capture/getAll',
        headers: {
        'Content-Type': 'application/json'
        },
    }).then(function successCallback(response) {
      // Only populating finished captures
        $scope.captures = response.data.filter(capture =>
          capture.status === "finished");
    }, function errorCallback(response) {
        console.log('error retrieving captures');
    })
};
<<<<<<< HEAD

//var getRDSInstances = function($http, $scope) {
//    $http({
//        method: 'GET',
//        url: 'capture/listDBinstances',
//        headers: {
//            'Content-Type': 'application/json'
//        },
//    }).then(function successCallback(response) {
//        $scope.DBConnections = response.data;
//        console.log('success');
//    }, function errorCallback(response) {
//        console.log('error');
//    });
//};
=======
>>>>>>> origin
