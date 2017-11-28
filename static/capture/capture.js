//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

//app.controller('capture', ['$scope', '$location', '$modal', function($scope, $location, $modal) {
app.controller('capture', function ($scope, $location, $uibModal) {
   $scope.open = function () {
      console.log('opening pop up');
      var modalInstance = $uibModal.open({
         templateUrl: '/static/capture/addDatabaseModal.html',
         controller: function ($scope, $uibModalInstance) {
            $scope.ok = function () {
               $uibModalInstance.close();
            };

            $scope.cancel = function () {
               $uibModalInstance.dismiss('cancel');
            };
         }
      });
   }

   $scope.close = function () {
      $uibModalInstance.dismiss('cancel');
   }
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
