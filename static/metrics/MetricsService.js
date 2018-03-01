var app = angular.module('MyCRT');

app.factory('Metrics', function() {
    var metrics = [];
    var cpuChart;
    var readIOChart;
    var writeIOChart;
    var memoryChart;

    // array of colors to use for the metrics charts
    var colors = [
        'cornflowerblue',
        'tomato',
        'palegreen',
        'pink',
        'orange',
        'lemonchiffon',
        'aqua',
        'darkorchid',
        'lime',
        'red',
        'yellow',
        'violet'
    ];
    // array to keep track of used colors so line colors are unique
    var usedColors = [];


    return {
        getCPUChart : function() {
            return cpuChart;
        },
        setCPUChart : function(chart) {
            cpuChart = chart;
        },
        getReadIOChart : function() {
            return readIOChart;
        },
        setReadIOChart : function(chart) {
            readIOChart = chart;
        },
        getWriteIOChart : function() {
            return writeIOChart;
        },
        setWriteIOChart : function(chart) {
            writeIOChart = chart;
        },
        getMemoryChart : function() {
            return memoryChart;
        },
        setMemoryChart : function(chart) {
            memoryChart = chart;
        },
        getNextColor : function() {
            var availableColors = colors.filter(function(obj) { return usedColors.indexOf(obj) == -1; });
            usedColors.push(availableColors[0]);
            return availableColors[0];
        },
        removeUsedColor : function(color) {
            var index = usedColors.indexOf(color);
            if (index > -1) {
                usedColors.splice(index, 1);
            }
        }
    }
});