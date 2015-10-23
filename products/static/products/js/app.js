/**
 * Created by user on 05.10.15.
 */

angular
    .module('myApp', [
        'ngRoute',
        'ui.bootstrap',
        'ngAnimate',
        'ngResource',
        'myApp.services'
    ])
    .config(function ($httpProvider, $resourceProvider, $interpolateProvider, $routeProvider) {

        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

        $resourceProvider.defaults.stripTrailingSlashes = false;
        $interpolateProvider.startSymbol('[[').endSymbol(']]');

        $routeProvider.
            when('/', {
                templateUrl: '/products_ang/list/',
                controller: 'itemCtrl'
            }).
            when('/products', {
                templateUrl: '/products_ang/list/',
                controller: 'itemCtrl'
            }).
            when('/products/:itemId', {
                templateUrl: '/products_ang/show/',
                controller: 'ItemDetailCtrl'
            }).
            when('/products/:itemId/edit', {
                templateUrl: '/products_ang/edit/',
                controller: 'ItemDetailCtrl'
            }).
            when('/products/:itemId/comments', {
                templateUrl: '/products_ang/comments/',
                controller: 'CommentsController'
            }).
            when('/products/:itemId/action/add', {
                templateUrl: '/products_ang/action/add/',
                controller: 'ActionCtrl'
            }).
            otherwise({
                redirectTo: '/'
            });

    });

