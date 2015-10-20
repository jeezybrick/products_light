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
            when('/products_ang/', {
                templateUrl: '/products_ang/',
                controller: 'itemCtrl'
            }).
            when('/:itemId', {
                templateUrl: '/products_ang/show/',
                controller: 'ItemDetailCtrl'
            }).
            when('/:itemId/edit', {
                templateUrl: '/products_ang/edit/',
                controller: 'ItemDetailCtrl'
            }).
             when('/:itemId/comments', {
                templateUrl: '/products_ang/comments/',
                controller: 'CommentsController'
            }).
            when('/:itemId/action/add', {
                templateUrl: '/products_ang/action/add/',
                controller: 'ActionCtrl'
            });

    });

