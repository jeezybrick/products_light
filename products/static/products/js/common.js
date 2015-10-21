/**
 * Created by user on 28.09.15.
 * For item on Django views, not Angular
 */
var clock;
clock = $('#clock').FlipClock({
          clockFace: "DailyCounter",
          autoStart: false

      });

      clock.setTime(5000);
      clock.setCountdown(true);
      clock.start(function(){});
  $(document).ready(function () {


    $('.notes').mouseenter(function () {
        $(this).removeClass('animated bounceInDown').addClass('animated pulse');

    }).mouseleave(function () {
        $(this).removeClass('animated pulse');
    });

      $('.messenger').delay(2000).slideUp();


      clock = $('#clock').FlipClock({
          clockFace: "DailyCounter",
          autoStart: false

      });

      clock.setTime(5000);
      clock.setCountdown(true);
      clock.start(function(){});
});