//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

app.controller('home', function($scope, $location, $http, activeNavItem) {
  $scope.showAll = true;
  $scope.showCaptures = false;
  $scope.showReplays = false;

  $scope.setCaptureActive = function(item) {
    activeNavItem.clearAndMakeItemActive('captureTab');
  }

  $scope.goCapture = function () {
    $location.path('/capture');
  }

  $scope.promptDelete = function(item) {
    if (item) {
      $scope.itemName = item.name;
      $scope.itemObj = item;
      $('#deleteModal').modal('show');
    }
  }

  $scope.deleteItem = function(item) {
    if (item.type == "capture") {
      this.deleteCapture(item.id)
    }
    else if (item.type == "replay") {
      this.deleteReplay(item.id)
    }
    $('#deleteModal').modal('hide');
  }

  $scope.showInfo = function(item) {
    if (item) {
      $scope.itemName = item.name;
      $scope.infoItem = item;
      $('#informationHomeModal').modal('show');
    }
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
      populateFinishedCapturesAndReplays($http, $scope);
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
      populateFinishedCapturesAndReplays($http, $scope);
    }, function errorCallback(response) {
      console.log('error');
    });
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
    this.filter(['#filter-all'], ['#filter-replays','#filter-captures'], true, false, false);
  }

  $scope.filterReplays = function() {
    this.filter(['#filter-replays'], ['#filter-captures','#filter-all'], false, false, true);
  }

  $scope.filterCaptures = function() {
    this.filter(['#filter-captures'], ['#filter-replays','#filter-all'], false, true , false);
  }

  $scope.filter = function(activeIds, inactiveIds, showAll, showCaptures, showReplays) {
    for (activeId in activeIds) {
      $(activeIds[activeId]).addClass('active');
    }
    for (inactiveId in inactiveIds) {
      $(inactiveIds[inactiveId]).removeClass('active');
    }
    $scope.showAll = showAll;
    $scope.showCaptures = showCaptures;
    $scope.showReplays = showReplays;
  }


  populateFinishedCapturesAndReplays($http, $scope);
  populateActiveCaptures($http, $scope);
  populateScheduledCaptures($http, $scope);

});
var options = {
  year: 'numeric',
  month: '2-digit',
  day: '2-digit',
  hour: '2-digit',
  minute: '2-digit'
};


var populateFinishedCapturesAndReplays = function($http, $scope) {
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
  }, function errorCallback(response) {
    console.error('error retrieving captures');
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
  }, function errorCallback(response) {
    console.log('error retrieving captures');
  })
};

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
