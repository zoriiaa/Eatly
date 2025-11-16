$(function () {
  $('.slider').slick({
    slidesToShow: 3,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 2000,
    speed: 800,
    cssEase: 'ease-in-out',
    prevArrow:
      '<button type="button" class="slick-prev"><img src="images/arrowL.svg" alt=""></button>',
    nextArrow:
      '<button type="button" class="slick-next"><img src="images/arrowR.svg" alt=""></img></button>',
  });

  $('.slider_days').slick({
    speed: 500,
    cssEase: 'ease-in-out',
    prevArrow:
      '<button type="button" class="slick-prev-day"><img src="images/Al.svg" alt=""></button>',
    nextArrow:
      '<button type="button" class="slick-next-day"><img src="images/Ar.svg" alt=""></img></button>',
  });
});
