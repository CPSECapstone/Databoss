//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

app.controller('replay', function($scope, $http, $location) {
    console.log("in replay");
    const dateContainer = $('#date-container');
    const timeContainer = $('#time-container');
    const storageContainer = $('#storage-container');

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

    var today = new Date(new Date().getFullYear(), new Date().getMonth(), new Date().getDate());
    $('#startDate').datepicker({
      uiLibrary: 'bootstrap4',
      iconsLibrary: 'fontawesome',
      minDate: today,
      maxDate: function () {
        return $('#endDate').val();
      }
    });
    $('#endDate').datepicker({
      uiLibrary: 'bootstrap4',
      iconsLibrary: 'fontawesome',
      minDate: function () {
        return $('#startDate').val();
      }
    });
    $('#startTime').timepicker({
      uiLibrary: 'bootstrap4',
      iconsLibrary: 'fontawesome',
    });
    $('#endTime').timepicker({
      uiLibrary: 'bootstrap4',
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
                    'captureBucket' : $('#crBucket').val(),
                    'dbName' : $('#dbName').val(),
                    'startDate' : $('#startDate').val(),
                    'endDate' : $('#endDate').val(),
                    'startTime' : $('#startTime').val(),
                    'endTime' : $('#endTime').val(),
                    'replayMode' : $('input[name=replayMode]:checked').val()
                }
            });
      // Add code to turn on DB logging here
      console.log("starting Replay!")
      $location.path('/progress');
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

    populateCaptures($http, $scope);
    getDBConnections($http, $scope);

});

var populateCaptures = function($http, $scope) {
    $http({
        method: 'GET',
        url: 'capture/getAll',
        headers: {
        'Content-Type': 'application/json'
        },
    }).then(function successCallback(response) {
        $scope.captures = response.data;
        calculateProgress($scope.captures);
        console.log('success');
    }, function errorCallback(response) {
        console.log('error retrieving captures');
    })
};
var getDBConnections = function($http, $scope) {
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

