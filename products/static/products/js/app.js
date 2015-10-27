/**
 * Created by user on 05.10.15.
 */

angular
    .module('myApp', [
        'ngRoute',
        'ui.router',
        'ui.bootstrap',
        'ngAnimate',
        'ngResource',
        'myApp.services',
        'flash',
        'mgcrea.ngStrap',
        'ngMaterial'
    ])
    .config(function ($httpProvider, $resourceProvider, $interpolateProvider, $routeProvider, $compileProvider, $stateProvider, $urlRouterProvider) {

        // CSRF Support
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

        $resourceProvider.defaults.stripTrailingSlashes = false;

        // Force angular to use square brackets for template tag
        // The alternative is using {% verbatim %}
        $interpolateProvider.startSymbol('[[').endSymbol(']]');

        $compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|ftp|mailto|chrome-extension):/);
        /*
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
            when('/products/:itemId/action/add', {
                templateUrl: '/products_ang/action/add/',
                controller: 'ActionCtrl'
            }).
            otherwise({
                redirectTo: '/'
            });
        */

        // Routing
        $urlRouterProvider.otherwise('/');
        $stateProvider
            .state('home', {
                url: '/',
                templateUrl: 'static/products/partials/home.html',
                controller: 'HomeController'
            })
            .state('products-list', {
                url: '/products',
                templateUrl: '/products_ang/list/',
                controller: 'itemCtrl'
            })
            .state('products-detail', {
                url: '/profile/:userId',
                templateUrl: 'static/tweeter/partials/profile.html',
                controller: 'UserCtrl'
            })

    });

