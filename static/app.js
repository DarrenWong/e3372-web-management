'use strict';

 var app = angular.module('myApp', ['ngRoute','statusList']);
 app.controller('myCtrl', function($scope, $http) {
 	$scope.welcome = "data";
 	$scope.sendDataOn = function(){
       $http({
          method: "POST",
          url: 'dataswitch',
          data: { 'dataswitch' : "1" }
        })
        .then(function(response) {
            $scope.welcome = "dataOn";
        });
       };
 	$scope.sendDataoff = function(){
       $http({
          method: "POST",
          url: 'dataswitch',
          data: { 'dataswitch' : "0" }
        })
        .then(function(response) {
            $scope.welcome = "dataOff";
        });
     };
      $scope.submit = function() {
        $http({
          method: "POST",
          url: "sendSMS",
          data: { 'number' : '59326208', 'SMStext':  'hellodarren'}
        })
        .then(function(response) {
            $scope.welcome = "sent already";
        });
      };
        //}
 	}
 );