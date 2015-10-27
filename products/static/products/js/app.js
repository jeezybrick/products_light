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
        'ngMaterial',
        'angular-loading-bar',
        'angular.filter',

    ])
    .config(function ($locationProvider, $httpProvider, $resourceProvider, $interpolateProvider, $routeProvider,
                      $compileProvider, $stateProvider, $urlRouterProvider) {

        // CSRF Support
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

        $resourceProvider.defaults.stripTrailingSlashes = false;

        // Force angular to use square brackets for template tag
        // The alternative is using {% verbatim %}
        $interpolateProvider.startSymbol('[[').endSymbol(']]');

        $compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|ftp|mailto|chrome-extension):/);

        // enable html5Mode for pushstate ('#'-less URLs)
        $locationProvider.html5Mode(true);
        $locationProvider.hashPrefix('!');


        // Routing
        $urlRouterProvider.otherwise('/');
        $stateProvider
            .state('auth-login', {
                url: '/login',
                templateUrl: '/static/my_auth/partials/login.html',
                controller: 'LoginCtrl'
            })
            .state('home', {
                url: '/',
                templateUrl: '/static/products/partials/home.html',
                controller: 'HomeController'
            })
            .state('products-list', {
                url: '/products/',
                templateUrl: '/products_ang/list/',
                controller: 'ItemController'
            })
            .state('products-detail', {
                url: '/products/:itemId/',
                templateUrl: '/products_ang/show/',
                controller: 'ItemDetailController'
            })
            .state('categories-list', {
                url: '/categories/',
                templateUrl: '/categories_ang/',
                controller: 'CategoryListController'
            })
            .state('shop-list', {
                url: '/shops/',
                templateUrl: '/static/products/partials/shop-list.html',
                controller: 'ShopListController'
            })
            .state('shop-detail', {
                url: '/shops/:id/',
                templateUrl: '/static/products/partials/shop-detail.html',
                controller: 'ShopDetailController'
            })


    });

