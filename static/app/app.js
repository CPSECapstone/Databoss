'use strict';

var app = angular.module('MyCRT', ['ngRoute', 'ui.bootstrap']);

//Models the href functionality of a link but for Angular routing.
//Use go-click="somewhere" in code to jump to a new view
app.directive('goClick', function ( $location ) {
   return function ( scope, element, attrs ) {
      var path;

      attrs.$observe('goClick', function (val) {
         path = val;
      });

      element.bind('click', function () {
         scope.$apply( function () {
            $location.path( path );
         });
      });
   };
});

//This is how Angular determines what page to display based on the URL.
//Note: The controller will be in the same parent folder as the templateUrl but in the js folder
//"css" value is optional
app.config(['$routeProvider', function($routeProvider) {
   $routeProvider
   //This is the home page
   .when('/', {
      templateUrl: 'static/app/login.html',
      controller: 'login',
      css: 'static/css/login.css'
   })
   .when('/capture', {
      templateUrl: 'static/capture/capture.html',
      controller: 'capture'
   })
   .when('/home', {
      templateUrl: 'static/home/home.html',
      controller: 'home'
   })
   .when('/information', {
      templateUrl: 'static/home/information.html',
      controller: 'information'
   })
   //If none of the "when"s are matched then it defaults to the home page.
   .otherwise({
      redirectTo: '/'
   });
}]);
