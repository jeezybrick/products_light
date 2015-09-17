/**
 * Created by user on 14.09.15.
 */

var myApp = angular.module('myApp', ['ngRoute']).config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

myApp.config(function($routeProvider) {
        $routeProvider.
          when('/:itemId', {
            templateUrl: 'api/products/show.html',
            controller: 'ItemDetailCtrl'
          });
});

myApp.controller('itemCtrl', function ($scope, $http) {

    $scope.sortField = '-id';
    $scope.reverse = true;
    $scope.showTriangle = false;
    $scope.showDetailOfItem = false;

      $http.get('/api/items/').success(function (data) {

            $scope.items = data;

      });

    $scope.showItem = function (id) {

        $http.get('/api/items/'+id+'?format=json').success(function (data) {

            $scope.itemDetail = data;
            $scope.showDetailOfItem = true;

      });

    };

});

myApp.controller('ItemDetailCtrl', function ($scope, $routeParams, $http){
        $scope.id = $routeParams.itemId;
        $scope.test = 'TEST';

        $http.get('/api/items/').success(function(data) {

          var item = data.filter(function(entry){
            return entry.id === $scope.id;
          })[0];

        });
});

myApp.controller('categoryListCtrl', function ($scope, $http) {

      $http.get('/api/categories/').success(function (data) {
          $scope.arr = [];
          $scope.arr_sub = [];
          $scope.categories = data;

          for(var i = 0;i<data.length;i++){

              if(data[i].parent_category == null){
                  $scope.arr.push(data[i]);
                  for(var j = 0;j<data.length;j++){
                      //console.log(data[i].id);
                      console.log(data[j].parent_category_id);
                      if(data[j].parent_category == data[i].id){
                          $scope.arr_sub.push(data[j]);
                      }
                  }
              }
          }

      });

});
