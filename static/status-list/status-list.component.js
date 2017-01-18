'use strict';

// Register `statusList` component, along with its associated controller and template
angular.
  module('statusList').
  component('statusList', {
    templateUrl: '/static/status-list/status-list.template.html',
    controller: function PhoneListController($scope, $http) {
      $scope.dataSwitch = "";
      $scope.deviceName = "";
      $scope.ispName = "";

      $http({
        method: 'GET',
        url: '/getdata'
      }).then(function successCallback(response) {
          $scope.phones =  response.data
          $scope.dataSwitch =  $scope.phones.dataswitch
          $scope.deviceName =  $scope.phones.devicename
          $scope.ispName =  $scope.phones.FullName

        }, function errorCallback(response) {
          // called asynchronously if an error occurs
          // or server returns response with an error status.
        }); 

      $scope.sendDataOn = function(){
         $http({
            method: "POST",
            url: 'dataswitch',
            data: { 'dataswitch' : "1" }
          })
          .then(function(response) {
              $scope.dataSwitch = "1"
          });
         };

      $scope.sendDataoff = function(){
         $http({
            method: "POST",
            url: 'dataswitch',
            data: { 'dataswitch' : "0" }
          })
          .then(function(response) {
              $scope.dataSwitch = "0";
          });
       };

       $scope.submit = function() {
            $http({
              method: "POST",
              url: "sendsms",
              data: { 'number' : this.number, 'SMStext':  this.smstext}
            })
            .then(function(response) {
                $scope.Send_SMS = response.data;
          });
        };
    }
 });
