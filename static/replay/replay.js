//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

app.controller('replay', function($scope, $http, $location, activeNavItem) {
  const dateContainer = $('#date-container');
  const timeContainer = $('#time-container');
  const storageContainer = $('#storage-container');

  var username;
  var password;
  var previousRds = $scope.rdsInstance;
  var authenticated = false;

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
    $('body').addClass('waiting');
    console.log("STARTING REPLAY-----");

    var replayName = $('#replayName').val();
    replayName = replayName.trim();

    $http({
      method: 'POST',
      url: 'replay/startReplay',
      headers: {
        'Content-Type' : 'application/json'
      },
      data : {
        'replayName' : replayName,
        'capture' : $('#capture').val(),
        'dbName' : 'no longer used',
        'username': username,
        'password': password,
        'startDate' : $('#startDate').val(),
        'endDate' : $('#endDate').val(),
        'startTime' : $('#startTime').val(),
        'endTime' : $('#endTime').val(),
        'replayMode' : $('input[name=replayMode]:checked').val()
      }
    })
    .then(function successCallback(response) {
      activeNavItem.clearAndMakeItemActive('replayTab');
      console.log("successful replay post");
      console.log("Some here other replay mode checked")
      // $location.path('home')
      $('body').removeClass('waiting');
      $location.path('replayProgress').search({name : replayName});
    })
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
      authenticated = false;
    }
  };

  $('#authenticationModal').on('shown.bs.modal', function () {
        $('#username').focus();
    });

  $('#authenticationModal').on('hide.bs.modal', function () {
      console.log("hiding modal");
      console.log(username);
      console.log(password);
      console.log($scope.username);
      console.log($scope.password);

      if (!authenticated) {
          console.log("Revert back to previous rds");
          $scope.$apply(function() {
              $scope.rdsInstance = previousRds;
          });
      }

      if ($scope.rdsInstance) {
          authenticated = true;
      }
  });

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
        $scope.instanceDbs = response.data;
        username = $scope.username;
        password = $scope.password;
        $scope.username = undefined;
        $scope.password = undefined;
        authenticated = true;
        $('#authenticationModal').modal('hide');
        previousRds = $scope.rdsInstance;
        console.log('success');
      }, function errorCallback(response) {
        $scope.instanceDbs = 'false';
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
