/**
 * Created by user on 05.10.15.
 */

myApp.controller('itemCtrl', function itemCtrl($scope, $http, Item, Category) {

    $scope.sortField = 'pk';
    $scope.reverse = true;
    $scope.showTriangle = false;
    $scope.showDetailOfItem = false;
    $scope.isCollapsed = true;
    $scope.itemLoad = false;

    /**
     * Get list of items and list of categories
     */

    $http.get(apiURLs.itemListUrl + jsonFormat, {cache: true}).success(function (data) {

        $scope.items = data;
        var myEl = angular.element(document.querySelector('.wrapperOnList'));
        myEl.removeClass('hidden');

        Category.query(function (response) {

            $scope.categories = response;
            $scope.itemLoad = true;

        });


    });

    /**
     * Show item detail
     */

    $scope.showItem = function () {
        $scope.showDetailOfItem = true;

    };

    /**
     * Filter items by category
     */

    $scope.sortByCategory = function (name) {
        $http.get(apiURLs.itemListUrl, {
            params: {
                category: name
            },
            cache: true

        }).success(function (data) {

            $scope.items = data;

        });

    };

    /**
     * Show all items
     */

    $scope.showAllItems = function () {
        $http.get(apiURLs.itemListUrl + jsonFormat, {cache: true}).success(function (data) {

            $scope.items = data;

        });

    };

    /**
     * Pagination
     */

    $scope.pagination = function (page) {

        $http.get(page, {cache: true}).success(function (data) {

            $scope.items = data;

        });

    };

    /**
     * For sorting by price
     */

    $scope.changeSortState = function (status) {
        $scope.sortField = status;
        $scope.reverse = !$scope.reverse;
        $scope.showTriangle = !$scope.showTriangle;
    };

    /**
     * Function for check if previous page exists
     */
    $scope.isItemsNotPrevious = function (items) {

        return !items.previous;

    };

    /**
     * Function for check if next page exists
     * @return {boolean}
     */
    $scope.IsItemsNotNext = function (items) {

        return !items.next;
    };


    $scope.getLocation = function (val) {
        return $http.get(apiURLs.itemListUrl, {
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

/**
 * Filter for pagination comments
 */

myApp.filter('startFrom', function () {
    return function (data, start) {
        if (angular.isDefined(data)) {
            return data.slice(start)
        }
    }
});


myApp.controller('ItemDetailCtrl', function ($scope, $routeParams, $http, $location, $window, $timeout, Item, Rate, Comment) {
    $scope.id = $routeParams.itemId;
    $scope.showDetailOfItem = true;
    $scope.greet = false;
    $scope.maxx = 100;
    $scope.dynamic = 0;
    $scope.itemDetailLoad = false;
    $scope.pageSize = 4;
    $scope.currentPage = 1;

    /**
     * Get item detail
     */
    Item.get({id: $routeParams.itemId}, function (data) {

        $scope.itemDetail = data;
        $scope.itemDetailLoad = true;
        $scope.rate = data['user_rate'];
        var myEl = angular.element(document.querySelector('.wrapperOnList'));
        myEl.removeClass('hidden');
    });

    // $scope.rate = 5;
    $scope.max = 10;
    $scope.isReadonly = false;

    /**
     * For hovering rating stars
     */
    $scope.hoveringOver = function (value) {
        $scope.overStar = value;
        $scope.percent = 100 * (value / $scope.max);
    };

    /**
     * Post selected rating of item by user
     */
    $scope.addRate = function () {
        $scope.dynamic = 100;
        var rate = new Rate({value: $scope.rate,
                            item: $routeParams.itemId});
        rate.$save(function () {
           // $scope.tweets.unshift(tweet);
        });

    };

     /**
     * Add comment
     */
    $scope.addComment = function () {

        var comment = new Comment({username: $scope.username,
                                   message: $scope.message,
                                   item: $routeParams.itemId });
        comment.$save(function (data) {
            $scope.hideCommentForm = true;
            $scope.appendComment = data;
            $scope.errorComment = false;
        });

    };

     /**
     * Edit item
     */
    $scope.editItem = function () {
        /*
        var item = Item.get({id: $routeParams.itemId});
        Item.update({ name:'LAL' }, item);
       */
        var editData = {
            name: $scope.itemDetail.name,
            price: $scope.itemDetail.price,
            image_url: $scope.itemDetail.image_url,
            description: $scope.itemDetail.description
        };
        $http.put(apiURLs.itemListUrl + $scope.id + '/', editData).success(function () {

            $scope.successAction();

        }).error(function (error) {
            $scope.errorEditItem = error;
        });
    };

     /**
     * Delete item
     */
    $scope.deleteItem = function () {

        if (confirm('Are you sure you want to delete this item?')) {

            $http.delete(apiURLs.itemListUrl + $scope.id + '/').success(function () {
                $scope.showDetailOfItem = false;
                // $location.path("/");
                $window.location.href = '/products_ang/';
            }).error(function (error) {
                $scope.errorDeleteItem = error;
            });
        }
    };

     /**
     * Function for success edit item
     */
    $scope.successAction = function () {

        $scope.editItemSuccess = true;
        $timeout.cancel($scope.time);

        $scope.time = $timeout(function () {

            $scope.editItemSuccess = false;

        }, 3000);

    };
});


myApp.controller('categoryListCtrl', function ($scope, Category) {

    /**
     * Get category list
     */

    Category.query(function (response) {

        $scope.categories = response;
        $scope.categoryLoad = true;
        var myEl = angular.element(document.querySelector('.wrapperOnList'));
        myEl.removeClass('hidden');

    });

});

myApp.controller('loginCtrl', function ($scope) {


});