/**
 * Created by user on 14.09.15.
 */

var myApp = angular.module('myApp', ['ngRoute', 'ui.bootstrap']).config(function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

myApp.config(function ($routeProvider) {
    $routeProvider.
        when('/products_ang/', {
            templateUrl: '/products_ang/',
            controller: 'itemCtrl'
        }).
        when('/:itemId', {
            templateUrl: '/products_ang/show/',
            controller: 'ItemDetailCtrl'
        })/*.
     otherwise({
     redirectTo: '/products_ang/'
     })*/;
});


myApp.controller('itemCtrl', function ($scope, $http) {

    $scope.sortField = 'pk';
    $scope.reverse = true;
    $scope.showTriangle = false;
    $scope.showDetailOfItem = false;
    $scope.isCollapsed = true;
    $scope.itemLoad = false;

    $http.get('/api/items/', {cache: true}).success(function (data) {

        $scope.items = data;
        var myEl = angular.element(document.querySelector('.wrapperOnList'));
        myEl.removeClass('hidden');

        $http.get('/api/categories/').success(function (data) {

            $scope.categories = data;
            $scope.itemLoad = true;

        });


    });

    $scope.showItem = function () {
        $scope.showDetailOfItem = true;

    };

    $scope.sortByCategory = function (name) {
        $http.get('/api/items/?category=' + name, {cache: true}).success(function (data) {

            $scope.items = data;

        });

    };

    $scope.showAllItems = function () {
        $http.get('/api/items/', {cache: true}).success(function (data) {

            $scope.items = data;

        });

    };

    $scope.pagination = function (page) {

        $http.get(page, {cache: true}).success(function (data) {

            $scope.items = data;

        });

    };

    $scope.getLocation = function (val) {
        return $http.get('/api/items/', {
            params: {
                category: val
            },
            cache: true

        }).then(function (response) {
            return response.data.results.map(function (item) {
                return item.name;
            });
        });
    };


});

myApp.filter('startFrom', function () {
    return function (data, start) {
        if (data != undefined) {
            return data.slice(start)
        }
    }
});

myApp.controller('ItemDetailCtrl', function ($scope, $routeParams, $http) {
    $scope.id = $routeParams.itemId;
    $scope.greet = false;
    $scope.maxx = 100;
    $scope.dynamic = 0;
    $scope.itemDetailLoad = false;
    $scope.pageSize = 4;
    $scope.currentPage = 1;

    $http.get('/api/items/' + $routeParams.itemId + '/?format=json', {cache: true}).success(function (data) {

        $scope.itemDetail = data;
        $scope.itemDetailLoad = true;
        $scope.rate = data['user_rate'];
        var myEl = angular.element(document.querySelector('.wrapperOnList'));
        myEl.removeClass('hidden');

    });
    // $scope.rate = 5;
    $scope.max = 10;
    $scope.isReadonly = false;

    $scope.hoveringOver = function (value) {
        $scope.overStar = value;
        $scope.percent = 100 * (value / $scope.max);
    };


    $scope.addRate = function () {
        $scope.dynamic = 100;
        var data = {
            "value": $scope.rate,
            "item": $scope.id
        };

        $http.post('/api/rates/', data).success(function (data) {
            $scope.greet = true;

        });
    };

    $scope.addComment = function () {
        var data = {
            "username": $scope.username,
            "message": $scope.message,
            "item": $scope.id
        };
        $http.post('/api/comments/', data).success(function () {
            $scope.hideCommentForm = true;
            $scope.appendComment = data;
            $scope.errorComment = false;

        }).error(function (data) {
            $scope.errorComment = data;
        });
    };
});

myApp.controller('categoryListCtrl', function ($scope, $http) {

    $http.get('/api/categories/').success(function (data) {

        $scope.categories = data;
        $scope.categoryLoad = true;
        var myEl = angular.element(document.querySelector('.wrapperOnList'));
        myEl.removeClass('hidden');

    });

});