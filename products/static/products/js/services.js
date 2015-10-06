/**
 * Created by user on 05.10.15.
 */


angular.module('myApp.services', ['ngResource'])
    .factory('Item', function ($resource) {
        return $resource('/api/items/:id/', { id: '@id' }, {
            'update': {method: 'PUT'},
            'query': {method: 'GET', isArray: false},
            'get':{method: 'GET', cache: true}
        });
    })
    .factory('User', function ($resource) {
        return $resource('/api/users/:id/');
    })
    .factory('Category', function ($resource) {
        return $resource('/api/categories/:id/');
    })
    .factory('Rate', function ($resource) {
        return $resource('/api/rates/:id/');
    })
    .factory('Comment', function ($resource) {
        return $resource('/api/comments/:id/');
    })

    .factory('Cart', function ($resource) {
        return $resource('/api/cart/:id/',
            {
                id: '@id'
            },
            {
                update: {
                    method: 'PUT'
                }
            }
        )
    });
