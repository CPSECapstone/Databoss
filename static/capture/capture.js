//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

//app.controller('capture', ['$scope', '$location', '$modal', function($scope, $location, $modal) {
app.controller('capture', function ($scope, $location, $uibModal, $http) {
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
   };

   $scope.getDBConnections = function() {
      console.log("getting db connections");

      $http({
         method: 'GET',
         url: '/dbc/get',
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
});

//var app = angular.module('MyCRT');
//
//app.controller('modal', ['$scope','$modal',function ($scope, $modal) {
//   $scope.open = function () {
//      console.log('opening pop up');
//      var modalInstance = $modal.open({
//         templateUrl: 'captureModal.html',
//      });
//   }
//}]);