/**
 * Created by user on 05.10.15.
 */

myApp.controller('itemCtrl', function itemCtrl($scope, $http, Item, Category, Cart) {

    // sort
    $scope.sortField = 'pk';
    $scope.reverse = true;
    $scope.showTriangle = false;

    $scope.showDetailOfItem = false;
    $scope.isCollapsed = true;
    $scope.itemLoad = false;

    /**
     * Get list of items and list of categories
     */


    $scope.items = Item.query(function () {

        $scope.itemLoad = true;

        $scope.categories = Category.query(function () {

                $scope.categoryLoad = true;

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

        $scope.items = Item.query(
            params={category: name}
        );

    };

    /**
     * Show all items
     */

    $scope.showAllItems = function () {

        $scope.items = Item.query();

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

    /**
     * Add item to cart and query Item object
     */

    $scope.addItemToCart = function (itemId) {

        $scope.cart = new Cart();
        $scope.cart.item = itemId;

        $scope.cart.$save(function () {

           $scope.items = Item.query();

        });

    };

    /**
     * Delete item form cart and query Item object
     */

    $scope.deleteItemInCart = function (itemId) {

        Cart.delete({ id: itemId }, function() {

            $scope.items = Item.query();

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

    $scope.id = $routeParams.itemId; // item id
    $scope.showDetailOfItem = true;
    $scope.itemDetailLoad = false;

    //message after rate item
    $scope.greet = false;

    //progressbar
    $scope.maxx = 100;
    $scope.dynamic = 0;

    //pagination for comments
    $scope.pageSize = 4;
    $scope.currentPage = 1;

    //rating
    $scope.max = 10;
    $scope.isReadonly = false;

    /**
     * Get item detail
     */
    $scope.itemDetail = Item.get({id: $routeParams.itemId}, function () {

        $scope.itemDetailLoad = true;
        $scope.rate = $scope.itemDetail.user_rate;

    });

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
        $scope.rateObject = new Rate({value: $scope.rate,
                            item: $routeParams.itemId});
        $scope.rateObject.$save(function () {
           // $scope.tweets.unshift(tweet);
        });

    };

     /**
     * Add comment
     */
    $scope.addComment = function () {

        $scope.commentObject = new Comment({username: $scope.username,
                                            message: $scope.message,
                                            item: $routeParams.itemId
        });

        $scope.commentObject.$save(function (data) {
            $scope.hideCommentForm = true;
            $scope.appendComment = data;
            $scope.errorComment = false;
        },function(error){
             $scope.errorComment = error;
         });

    };

     /**
     * Edit item
     */

     $scope.editItem = function () {

         $scope.itemDetail.$update(function () {
             $scope.successAction();
         },function(error){
             $scope.errorEditItem = error;
         });

    };

     /**
     * Delete item
     */
    $scope.deleteItem = function () {

        bootbox.confirm("Are you sure you want to delete this item?", function (answer) {

            if (answer == true)

                $scope.itemDetail.$delete(function () {
                $scope.showDetailOfItem = false;
                $window.location.href = '/products_ang/';
            },function(error){
                $scope.errorDeleteItem = error;
            });

        });

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

    $scope.categories = Category.query(function () {

        $scope.categoryLoad = true;

    });

});

myApp.controller('CartCtrl', function ($scope, $window, $timeout, Cart) {

    $scope.addItemToCart = function (itemId) {

        var cart = new Cart();
        cart.item = itemId;

        cart.$save(function () {
           $scope.itemInTheCart = true;
        });

    };


    /**
     * Delete item form cart and query Item object
     */

    $scope.deleteItemInCart = function (itemId) {

        bootbox.confirm("Are you sure you want to delete this item from the cart?", function (answer) {

            if (answer == true)

                Cart.delete({id: itemId}, function () {

                    var myEl = angular.element(document.querySelector('#item_'+itemId));
                    myEl.addClass('animated fadeOut');

                    $scope.time = $timeout(function () {

                        myEl.addClass('hidden');

                    }, 800);

                });

        });

    };

    /**
     * Choose specific item in the cart
     */

    $scope.chooseItem = function (itemId) {

        var myEl = angular.element(document.querySelector('#item_'+itemId));
        myEl.toggleClass('panel-primary-active');

    };

     /**
     * Choose all items with button
     */
    $scope.toggleAll = function () {

        $scope.allItemActive = ! $scope.allItemActive;

    };

    /**
     * Choose all items with click 'All"
     */
    $scope.chooseAll = function () {

        $scope.allItemActive = true;

    };

    /**
     * Unchoose all items
     */
    $scope.chooseNothing = function () {

        $scope.allItemActive = false;

    };

    /**
     * Make order and show alert
     */
     $scope.makeOrder = function () {

         bootbox.alert("You make order! Soon we call you!");

    };

});

myApp.controller('loginCtrl', function ($scope) {


});