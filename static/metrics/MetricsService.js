var app = angular.module('MyCRT');

app.factory('Metrics', function() {
    var metrics = [];
    var cpuChart;
    var readIOChart;
    var writeIOChart;
    var memoryChart;

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
    }
});