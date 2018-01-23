//Initialize the angular application for this AngularJS controller
var app = angular.module('MyCRT');

//whenever an action occurs on the metrics page, the controller will handle it
app.controller('metrics', function($scope, $location, $http) {
    var time = [6, 7, 8, 9, 10, 11, 12]
    // For drawing the lines
    var cpu = [86, 114, 105, 140, 145, 151, 180]
    var ctx = document.getElementById("myChart");
    var myChart = new Chart(ctx, {
    type: 'line',
     data: {
       labels: time,
       datasets: [
         {
           data: cpu,
           label: "CPU",
           borderColor: 'rgba(10, 148, 255, 1)',
           backgroundColor:'rgba(10, 148, 255, 0.57)'
         }
       ]
     }
});

});