/**
 * Created by user on 28.09.15.
 * For item on Django views, not Angular
 */

  $(document).ready(function () {
        $('.notes').mouseenter(function () {
            $(this).removeClass('animated bounceInDown').addClass('animated pulse');

        }).mouseleave(function () {
            $(this).removeClass('animated pulse')
        });

        $('.messenger').delay(2000).slideUp();
    });