/**
 * Created by user on 05.10.15.
 */

angular
    .module('myApp')
    .controller('itemCtrl', itemCtrl);

function itemCtrl($scope, $http, Item, Category, Cart, Flash) {

    // sort init
    $scope.sortField = 'price';
    $scope.reverseSortFieldByPrice = '-price';
    $scope.sortFieldByPrice = 'price';
    $scope.reverse = true;
    $scope.showTriangle = false;

    //rating
    $scope.maxx = 10;
    $scope.isReadonly = false;

    //filter init
    $scope.search = { categories:undefined };

    $scope.showDetailOfItem = false;
    $scope.isCollapsed = true;
    $scope.itemLoad = false;

    //quantity of item
    $scope.minQuantityOfItem = 10;
    $scope.zeroQuantityOfItem = 0;

    //messages
    $scope.addItemToCartMessageSuccess = 'Item added to cart';
    $scope.deleteItemFromCartMessageSuccess = 'Item deleted from cart';

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

        if (page !== null) {
            $http.get(page, {cache: true}).success(function (data) {

                $scope.items = data;

            });
        }
    };

    /**
     * For sorting by price
     */
    $scope.changeSortState = function () {
        $scope.reverse = !$scope.reverse;

        if(angular.equals($scope.sortField, $scope.sortFieldByPrice)) {
            return $scope.sortField = '-price'
        }

        if(angular.equals($scope.sortField, $scope.reverseSortFieldByPrice)) {
            return $scope.sortField = 'price'
        }
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

            $scope.itemLoad = false;
            $scope.items = Item.query(function(){
                $scope.itemLoad = true;
            });
            $scope.itemInCartSuccess = true;
            Flash.create('success', $scope.addItemToCartMessageSuccess, 'flash-message-item-list');


        }, function (error) {

            $scope.itemInCartError = error.data.detail;
            Flash.create('danger', $scope.itemInCartError, 'flash-message-item-list');

        });

    };


    /**
     * Delete item form cart and query Item object
     */
    $scope.deleteItemInCart = function (itemId) {

        Cart.delete({id: itemId}, function () {
            $scope.itemLoad = false;
            $scope.items = Item.query(function(){
                $scope.itemLoad = true;
            });

            Flash.create('info', $scope.deleteItemFromCartMessageSuccess, 'flash-message-item-list');

        }, function(error){
            $scope.deleteItemfromCartError = error;
            Flash.create('danger', $scope.deleteItemfromCartError, 'flash-message-item-list');
        });
    };


    /**
     * Check if quantity of item is zero
     */
    $scope.isQuantityOfItemIsZero = function(item){

        return angular.equals($scope.zeroQuantityOfItem, item.quantity);
    };

    // title for aside nav
    $scope.aside = {
        "title": "Categories"
    };


    $scope.sortBy = function () {

        $scope.itemLoad=false;

        $scope.items = Item.query(
            params = {sort: $scope.sortField},function(){
                $scope.itemLoad=true;
            }
        );
    };


}

angular
    .module('myApp')
    .controller('ItemDetailCtrl', ItemDetailCtrl);

function ItemDetailCtrl($scope, $routeParams, $location, Item, Rate, AuthUser, Comment, Flash, $anchorScroll) {

    // Init
    $scope.id = $routeParams.itemId; // item id
    $scope.AuthUserUsername = AuthUser.username; // Auth user username
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
    $scope.itemDetailLoadError = false;
    $scope.successMessageEditItem = 'Item edit successfuly!<strong> Click</strong> to item page.';
    $scope.successMessageAddComment = 'Thanks for comment!';


    //add pre-comment model
    $scope.comment = {
        username:'Ivan',
        message:'Hello world!',
        item: $routeParams.itemId
    };


    /**
     * Get item detail
     */
    $scope.itemDetail = Item.get({id: $routeParams.itemId}, function (response) {

        $scope.itemDetailLoad = true;
        $scope.itemDetailComments = response.comments;


        /**
         * Add rate model
         */
        $scope.rate = {
            value: $scope.itemDetail.rates,
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
            $scope.rateError = error.data.detail;

            Flash.create('warning', $scope.rateError, 'flash-message-item-list');
        });

    };

    /**
     * Edit item
     */
    $scope.editItem = function () {

        $scope.itemDetail.$update(function (response) {
            $scope.successAction();
             $scope.itemDetail = response;

        }, function (error) {
            $scope.errorEditItem = error.data.detail;

            Flash.create('danger', $scope.errorEditItem, 'flash-message-item-list');
        });

    };

    /**
     * Delete item
     */
    $scope.deleteItem = function () {

        bootbox.confirm('Are you sure you want to delete this item?', function (answer) {

            if (answer === true)

                $scope.itemDetail.$delete(function () {

                    $scope.showDetailOfItem = false;
                    $location.path('/products');

                }, function (error) {
                    $scope.errorDeleteItem = error;
                });

        });

    };

    /**
     * Function for success edit item
     */
    $scope.successAction = function () {

        Flash.create('flash-message-edit-item', $scope.successMessageEditItem, 'flash-message-edit-item');

        $scope.editItemSuccess = true;

    };

    /**
     * Check is Auth user is owner of this item
     */
    $scope.isAuthUserIsOwner = function () {

        return $scope.AuthUserUsername === $scope.itemDetail.user;

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
            Flash.create('success', $scope.successMessageAddComment, 'flash-message-edit-item');

        }, function (error) {

            $scope.errorComment = error;
        });

    };

    /**
     * Scroll to add comments form
     */
    $scope.scrollTo = function (id) {
        var old = $location.hash();
        $location.hash(id);
        $anchorScroll();
        //reset to old to keep any additional routing logic from kicking in
        $location.hash(old);
    };

     /**
     * Return true if comments exists and number of comments bigger then pagesize
     */
    $scope.isCommentsLengthBiggerThenPagesize = function () {

        return $scope.itemDetailComments.length > $scope.pageSize;
    };
}

angular
    .module('myApp')
    .controller('CategoryListCtrl', CategoryListCtrl);

function CategoryListCtrl($scope, $http, Category, Flash) {


    /**
     * Get category list
     */
    $scope.categories = Category.query(function () {

        $scope.categoryLoad = true;

         /**
         * Function for check if previous page exists
         */
        $scope.isCategoriesNotPrevious = function () {

            return !$scope.categories.previous;

        };

        /**
         * Function for check if next page exists
         * @return {boolean}
         */
        $scope.IsCategoriesNotNext = function () {

            return !$scope.categories.next;
        };

    }, function (error) {
        $scope.categoryLoadError = error.data.detail;
        Flash.create('warning', $scope.categoryLoadError, 'flash-message-item-list');
    });


    /**
     * Pagination
     */
    $scope.pagination = function (page) {

        if (page !== null) {

            $http.get(page, {cache: true}).success(function (data) {

                $scope.categories = data;

            });
        }

    };

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
    vm.addItemToOrder = addItemToOrder;

    $scope.itemListForOrder = [];


    /**
     * Get list of items in the cart of the current auth user
     */
    $scope.cartObject = Cart.query(function () {

        $scope.cartLoad = true;

    }, function () {
        $scope.cartLoadError = true;
    });


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
     * Add item to order for purchase
     */
    function addItemToOrder(item) {
         var index = $scope.itemListForOrder.indexOf(item);

        if(index > -1){
            $scope.itemListForOrder.splice(index);
        }else{
           $scope.itemListForOrder.push(item);
        }


    }



    /**
     * Delete item form cart and query Item object
     */
    function deleteItemInCart(itemId) {

        bootbox.confirm('Are you sure you want to delete this item from the cart?', function (answer) {

            if (answer === true)

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

        var index = $scope.itemListForOrder.indexOf(itemId);

        if(index > -1){
            $scope.itemListForOrder.splice(index);
        }else{
           $scope.itemListForOrder.push(itemId);
        }

    }

    /**
     * Choose all items with button
     */
    function toggleAll() {

        $scope.allItemActive = !$scope.allItemActive;
        $scope.itemListForOrder = !$scope.itemListForOrder;

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
        $scope.itemListForOrder = [];

    }

    /**
     * Show alert after making order
     */
    function makeOrder() {

        bootbox.alert('You make order! Soon we call you!');

    }

}

angular
    .module('myApp')
    .controller('ActionCtrl', ActionCtrl);

function ActionCtrl($scope, $routeParams, $location, Action, AuthUser, Flash) {

    $scope.itemId = $routeParams.itemId;
    $scope.AuthUserUsername = AuthUser.username; // Auth user id

    // messages
    $scope.addActionSuccessMesage = 'Action modify!';

    /**
     * Get action for this item
     */

    $scope.action = Action.get({item_id: $routeParams.itemId}, function (data) {

        $scope.action = data;
        $scope.action.period_from = new Date($scope.action.period_from);
        $scope.action.period_to = new Date($scope.action.period_to);



    }, function (error) {

        $scope.actionError = error;

        /**
         *
         * Check if action for current item exists
         */
        $scope.doesActionNotExists = function () {

            return angular.equals($scope.actionError.status, 404);

        };

        /**
         * Check is permission denied
         */
        $scope.isPermissionDenied = function () {

            return angular.equals($scope.actionError.status, 403);
        };
    });


    /**
     * Add action
     */
    $scope.addAction = function () {

        $scope.actionObject = new Action({
            description: $scope.action.description,
            new_price: $scope.action.new_price,
            item: $scope.itemId,
            period_from: moment($scope.action.period_from).format('YYYY-MM-DD'),
            period_to: moment($scope.action.period_to).format('YYYY-MM-DD')
        });

        $scope.actionObject.$save(function () {

            Flash.create('success', $scope.addActionSuccessMesage, 'flash-message-item-list');
            $location.path('products/'+ $scope.itemId);

        }, function (error) {

            $scope.errorAddAction = error;
        });

    };

    /**
     * Delete action
     */
    $scope.deleteAction = function () {

        bootbox.confirm('Are you sure you want to delete this action?', function (answer) {

            if (answer === true)

                Action.delete({item_id: $routeParams.itemId}, function () {

                    $location.path('products/'+ $scope.itemId);

                });

        });

    };



}

angular
    .module('myApp')
    .controller('LoginCtrl', LoginCtrl);

function LoginCtrl($scope) {

//

}

angular
    .module('myApp')
    .controller('TestController', TestController);

function TestController($scope, Upload, $timeout) {

    /**
     * Function for upload image files
     */
    $scope.uploadPic = function (file) {
        file.upload = Upload.upload({
            url: 'https://angular-file-upload-cors-srv.appspot.com/upload',
            data: {file: file, username: $scope.username}
        });

        file.upload.then(function (response) {
            $timeout(function () {
                file.result = response.data;
            });
        }, function (response) {
            if (response.status > 0)
                $scope.errorMsg = response.status + ': ' + response.data;
        }, function (evt) {
            // Math.min is to fix IE which reports 200% sometimes
            file.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
        });
    }

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
