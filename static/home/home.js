//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

app.controller('home', function($scope, $location, $http, activeNavItem) {
  $scope.showAll = true;
  $scope.showCaptures = false;
  $scope.showReplays = false;
  $scope.setCaptureActive= function(item) {
    activeNavItem.clearAndMakeItemActive('captureTab');
  }

  $scope.goCapture = function () {
      $location.path('/capture');
  }


  $scope.deleteCapture = function(captureId) {
    $http({
        method: 'DELETE',
        url: 'capture/deleteCapture/' + captureId,
        headers: {
            'Content-Type': 'application/json'
        },
        data: {
            'captureId': captureId
        }
    }).then(function successCallback(response) {
        populateCapturesAndReplays($http, $scope);
        //$('#confirmModal').modal('hide')
        console.log('success');
    }, function errorCallback(response) {
        console.log('error');
    });
  }

  $scope.deleteReplay = function(replayId) {
    $http({
        method: 'DELETE',
        url: 'replay/deleteReplay/' + replayId,
        headers: {
            'Content-Type': 'application/json'
        },
        data: {
            'replayId': replayId
        }
    }).then(function successCallback(response) {
        populateCapturesAndReplays($http, $scope);
        //$('#confirmModal').modal('hide')
//        if (replay.status == 'finished') {
//            //$('#messageModal').modal('show')
//        }
        console.log('success');
    }, function errorCallback(response) {
        console.log('error');
    });
  }

  $scope.delete = function(id) {
    console.log("DELETE BUTTON PRESSED for " + id);
  }

  $scope.viewMetrics = function() {
    activeNavItem.clearAndMakeItemActive('metricsTab');
  }

  $scope.viewCaptureProgress = function() {
    activeNavItem.clearAndMakeItemActive('captureTab');
  }

  $scope.hoverOn = function() {
    this.isHovering = true;
  }

  $scope.hoverOff = function() {
    this.isHovering = false;
  }

  $scope.filterAll = function() {
    $("#filter-captures").removeClass('active');
    $("#filter-replays").removeClass('active');
    $("#filter-all").addClass('active');
    $scope.showAll = true;
    $scope.showCaptures = false;
    $scope.showReplays = false;
  }

  $scope.filterCaptures = function() {
    $("#filter-captures").addClass('active');
    $("#filter-replays").removeClass('active');
    $("#filter-all").removeClass('active');
    $scope.showAll = false;
    $scope.showCaptures = true;
    $scope.showReplays = false;
  }

  $scope.filterReplays = function() {
    $("#filter-replays").addClass('active');
    $("#filter-captures").removeClass('active');
    $("#filter-all").removeClass('active');
    $scope.showAll = false;
    $scope.showCaptures = false;
    $scope.showReplays = true;
  }

  populateCapturesAndReplays($http, $scope);
  populateActiveCaptures($http, $scope);
  // populateFinishedCaptures($http, $scope);
  populateScheduledCaptures($http, $scope);

});
var options = {
  year: 'numeric',
  month: '2-digit',
  day: '2-digit',
  hour: '2-digit',
  minute: '2-digit'
};


var populateCapturesAndReplays = function($http, $scope) {
  $http({
        method: 'GET',
        url: 'capture/getSortedCapturesAndReplays',
        headers: {
            'Content-Type': 'application/json'
        },
    }).then(function successCallback(response) {
      $scope.active = [];
      $scope.finished = [];
      response.data.captures.map((capture) => {
        capture.type = "capture";
        if (capture.status == "active") {
          $scope.active.push(capture);
        }
        else if (capture.status == "finished") {
          capture.passFail = "passed";
          $scope.finished.push(capture);
        } else if (capture.status == "failed") {
          capture.passFail = "failed";
          $scope.finished.push(capture);
        }
      })

      response.data.replays.map((replay) => {
        replay.type = "replay";
        if (replay.status == "active") {
          replay.progress = " ";
          $scope.active.push(replay);
        }
        else if (replay.status == "finished") {
          replay.passFail = "passed";
          $scope.finished.push(replay);
        }
      })
      formatDates($scope.finished);
      formatDates($scope.active);
      calculateProgress($scope.active);
      console.log(response.data.captures);
      console.log(response.data.replays);
    }, function errorCallback(response) {
        console.log('error retrieving captures');
    })
};

var populateActiveCaptures = function($http, $scope) {
    $http({
        method: 'GET',
        url: 'capture/active',
        headers: {
        'Content-Type': 'application/json'
        },
    }).then(function successCallback(response) {
        $scope.activeCaptures = response.data;
        calculateProgress($scope.activeCaptures);
        console.log('success');
    }, function errorCallback(response) {
        console.log('error retrieving captures');
    })
};

// var populateFinishedCaptures = function($http, $scope) {
//     $http({
//         method: 'GET',
//         url: 'capture/finished',
//         headers: {
//         'Content-Type': 'application/json'
//         },
//     }).then(function successCallback(response) {
//         $scope.finishedCaptures = response.data;
//         formatDates($scope.finishedCaptures);
//         console.log('success');
//     }, function errorCallback(response) {
//         console.log('error retrieving captures');
//     })
// };

var populateScheduledCaptures = function($http, $scope) {
    $http({
        method: 'GET',
        url: 'capture/scheduled',
        headers: {
        'Content-Type': 'application/json'
        },
    }).then(function successCallback(response) {
        $scope.scheduledCaptures= response.data;
        formatDates($scope.scheduledCaptures);
        console.log('success');
    }, function errorCallback(response) {
        console.log('error retrieving captures');
    })
};

var formatDates = function(captures) {
  for (var i = 0; i < captures.length; i++) {
    startTime = new Date(captures[i].startTime);
    startTime.setHours(startTime.getHours() + 7);
    endTime = new Date(captures[i].endTime);
    endTime.setHours(endTime.getHours() + 7);
    captures[i].formattedStart = startTime.toLocaleDateString('en-US', options);
    captures[i].formattedEnd = endTime.toLocaleDateString('en-US', options);
  }
};

var calculateProgress = function(captures) {
  var totalTimeMS = null;
  var startTime = null;
  var endTime = null;
  var elapsedTimeMS = null;
  var currentTime = null;
  var percentage = null;
  for (var i = 0; i < captures.length; i++) {
    if (captures[i].type == "capture") {
      startTime = new Date(captures[i].startTime);
      startTime.setHours(startTime.getHours() + 7);
      endTime = new Date(captures[i].endTime);
      endTime.setHours(endTime.getHours() + 7);
      totalTimeMS = endTime - startTime;
      currentTime = Date.now();
      elapsedTimeMS = currentTime - startTime;
      percentage = (elapsedTimeMS/totalTimeMS) * 100;
      captures[i].progress = percentage.toFixed(0) + "%";
      captures[i].formattedStart = startTime.toLocaleDateString('en-US', options);
      captures[i].formattedEnd = endTime.toLocaleDateString('en-US', options);
    }
    else {
      captures[i].progress =  0 + "%";
    }
  }
}
