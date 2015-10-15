/**
 * Created by user on 05.10.15.
 */

angular
    .module('myApp')
    .controller('itemCtrl', itemCtrl);

function itemCtrl($scope, $http, $timeout, Item, Category, Cart) {

    // sort init
    $scope.sortField = '-pk';
    $scope.reverse = true;
    $scope.showTriangle = false;

    //filter init
    $scope.search = { categories:undefined };

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

        }, function () {
            $scope.categoryLoadError = true;
        });


    }, function () {
        $scope.itemLoadError = true;
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
            params = {category: name}
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


    /**
     * Add item to cart and query Item object
     */
    $scope.addItemToCart = function (itemId) {

        $scope.cart = new Cart();
        $scope.cart.item = itemId;

        $scope.cart.$save(function () {

            $scope.items = Item.query();
            $scope.itemInCartSuccess = true;

            $scope.time = $timeout(function () {

                $scope.itemInCartSuccess = false;

            }, 2000);


        }, function (error) {
            $scope.itemInCartError = error.data.detail;
        });

    };


    /**
     * Delete item form cart and query Item object
     */
    $scope.deleteItemInCart = function (itemId) {

        Cart.delete({id: itemId}, function () {

            $scope.items = Item.query();

        });
    };

}


/**
 * Filter for pagination comments
 */
angular
    .module('myApp')
    .filter('startFrom', function () {
        return function (data, start) {
            if (angular.isDefined(data)) {
                return data.slice(start)
            }
        }
    });


angular
    .module('myApp')
    .controller('ItemDetailCtrl', ItemDetailCtrl);

function ItemDetailCtrl($scope, $routeParams, $window, $timeout, Item, Rate, Comment, AuthUser) {

    // Init
    $scope.id = $routeParams.itemId; // item id
    $scope.AuthUserUsername = AuthUser.username; // Auth user username
    $scope.showDetailOfItem = true;
    $scope.itemDetailLoad = false;

    //add pre-comment model
    $scope.comment = {
        username:'Ivan',
        message:'Hello world!1',
        item: $routeParams.itemId
    };

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

    $scope.itemDetailLoadError = false;

    /**
     * Get item detail
     */
    $scope.itemDetail = Item.get({id: $routeParams.itemId}, function () {

        $scope.itemDetailLoad = true;

        /**
         * Add rate model
         */
        $scope.rate = {
            value: $scope.itemDetail.user_rate,
            item: $routeParams.itemId
        };

    }, function (error) {

        $scope.itemDetailLoadError = error.data.detail;
    });


    /**
     * Add rate model
     */
     $scope.rate = {
        value: $scope.itemDetail.user_rate,
        item: $routeParams.itemId
    };

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

        $scope.rateObject = new Rate($scope.rate);

        $scope.rateObject.$save(function () {

            $scope.greet = true;
            $scope.dynamic = 100;

        }, function (error) {
            //
        });

    };

    /**
     * Add comment
     */
    $scope.addComment = function () {

        $scope.commentObject = new Comment($scope.comment);

        $scope.commentObject.$save(function (data) {
            $scope.hideCommentForm = true;
            $scope.appendComment = data;
            $scope.errorComment = false;
        }, function (error) {
            $scope.errorComment = error;
        });

    };

    /**
     * Edit item
     */
    $scope.editItem = function () {

        $scope.itemDetail.$update(function () {
            $scope.successAction();
        }, function (error) {
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
                }, function (error) {
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

    /**
     * Check is Auth user is owner of this item
     */
    $scope.isAuthUserIsOwner = function () {

        return $scope.AuthUserUsername === $scope.itemDetail.user;

    };

    /**
     * Return true if comments exists and number of comments bigger then pagesize
     */
    $scope.isCommentsExistsAndCommentsLengthBiggerThenPagesize = function () {

        return $scope.itemDetail.comments.length && $scope.itemDetail.comments.length > $scope.pageSize;

    };

}

angular
    .module('myApp')
    .controller('CategoryListCtrl', CategoryListCtrl);

function CategoryListCtrl($scope, Category) {


    /**
     * Get category list
     */
    $scope.categories = Category.query(function () {

        $scope.categoryLoad = true;

    }, function (error) {
        $scope.categoryLoadError = error.data.detail;
    });

}

angular
    .module('myApp')
    .controller('CartCtrl', CartCtrl);

function CartCtrl($scope, $timeout, Cart) {

    var vm = this;
    vm.deleteItemInCart = deleteItemInCart;
    vm.addItemToCart = addItemToCart;
    vm.chooseItem = chooseItem;
    vm.toggleAll = toggleAll;
    vm.chooseAll = chooseAll;
    vm.chooseNothing = chooseNothing;
    vm.makeOrder = makeOrder;


    /**
     * Add item to cart
     */
    function addItemToCart(itemId) {

        $scope.cart = new Cart();
        $scope.cart.item = itemId;

        $scope.cart.$save(function () {
            $scope.itemInTheCart = true;
        });

    }


    /**
     * Delete item form cart and query Item object
     */
    function deleteItemInCart(itemId) {

        bootbox.confirm("Are you sure you want to delete this item from the cart?", function (answer) {

            if (answer == true)

                Cart.delete({id: itemId}, function () {

                    var myEl = angular.element(document.querySelector('#item_' + itemId));
                    myEl.addClass('animated fadeOut');

                    $scope.time = $timeout(function () {

                        myEl.addClass('hidden');

                    }, 800);

                });

        });

    }

    /**
     * Choose specific item in the cart
     */

    function chooseItem(itemId) {

        var myEl = angular.element(document.querySelector('#item_' + itemId));
        myEl.toggleClass('panel-primary-active');

    }

    /**
     * Choose all items with button
     */
    function toggleAll() {

        $scope.allItemActive = !$scope.allItemActive;

    }

    /**
     * Choose all items with click 'All"
     */
    function chooseAll() {

        $scope.allItemActive = true;

    }

    /**
     * Unchoose all items
     */
    function chooseNothing() {

        $scope.allItemActive = false;

    }

    /**
     * Make order and show alert
     */
    function makeOrder() {

        bootbox.alert("You make order! Soon we call you!");

    }

}

angular
    .module('myApp')
    .controller('ActionCtrl', ActionCtrl);

function ActionCtrl($scope, $routeParams, $location, Action) {

    $scope.itemId = $routeParams.itemId;

    /**
     * Add action
     */
    $scope.addAction = function () {

        $scope.actionObject = new Action({
            description: $scope.description,
            new_price: $scope.new_price,
            item: $scope.itemId,
            period_from: $scope.period_from,
            period_to: $scope.period_to
        });

        $scope.actionObject.$save(function (response) {

            $location.path($scope.itemId);

        }, function (error) {

            $scope.errorAddAction = error;
        });

    };

}

angular
    .module('myApp')
    .controller('LoginCtrl', LoginCtrl);

function LoginCtrl($scope) {

//
}


/**
 * Directive for formatting date from datepicker Angular UI( add action form )
 */
angular
    .module('myApp')
    .directive('myDate', function (dateFilter, $parse) {
        return {
            restrict: 'EAC',
            require: '?ngModel',
            link: function (scope, element, attrs, ngModel, ctrl) {
                ngModel.$parsers.push(function (viewValue) {
                    return dateFilter(viewValue, 'yyyy-MM-dd');
                });
            }
        }
    });