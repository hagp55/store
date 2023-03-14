'use strict';


$(document).ready(function () {
  $('.header__list a').each(function () {
    let location = window.location.protocol + '//' + window.location.host + window.location.pathname;
    let link = this.href;
    if (location == link) {
      $(this).addClass('header__link-active');
    }
  });
})


function ajaxPagination() {
  $('#pagination a.page-link').each((index, el) => {
    $(el).click((e) => {
      e.preventDefault()
      let page_url = $(el).attr('href')
      $.ajax({
        url: page_url,
        type: 'GET',
        success: (data) => {
          $('#product_list').empty()
          $('#product_list').append($(data).find('#product_list').html())
          $('#pagination').empty()
          $('#pagination').append($(data).find('#pagination').html())
        }
      })
    })
  })
}

$(document).ready(function () {
  ajaxPagination()
})

$(document).ajaxStop(function () {
  ajaxPagination()
})


let thumbnails = document.getElementsByClassName('product__thumbnail')

let activeImages = document.getElementsByClassName('active')

for (var i = 0; i < thumbnails.length; i++) {

  thumbnails[i].addEventListener('mouseover', function () {
    if (activeImages.length > 0) {
      activeImages[0].classList.remove('active')
    }


    this.classList.add('active')
    document.getElementById('featured').src = this.src
  })
}

// let buttonRight = document.getElementById('slideRight');
// let buttonLeft = document.getElementById('slideLeft');

// buttonLeft.addEventListener('click', function () {
//   document.getElementById('slider').scrollLeft -= 180
// })

// buttonRight.addEventListener('click', function () {
//   document.getElementById('slider').scrollLeft += 180
// })



(function ($) {
  $('.product-slider').owlCarousel({
    loop: true,
    nav: true,
    dots: false,
    margin: 30,
    autoplay: true,
    responsive: {
      0: {
        items: 1,
      },
      480: {
        items: 2,
      },
      768: {
        items: 3,
      },
      1200: {
        items: 4,
      }
    }
  });
})(jQuery);


let header__burger = document.querySelector('.header__burger');
let header_menu = document.querySelector('.header__menu');
let header__list = document.querySelector('.header__list');

document.addEventListener('DOMContentLoaded', () => { // Структура страницы загружена и готова к взаимодействию

  const button = document.querySelector('.header__burger') // находим кнопку для открытия/закрытия окна навигации
  const nav = document.querySelector('.header__menu') // находим окно навигации

  button.addEventListener('click', () => { // при клике на кнопку
    header__burger.classList.toggle('active');
    header_menu.classList.toggle('active'); // открываем/закрываем окно навигации, добаляя/удаляя активный класс
  })

  window.addEventListener('click', e => { // при клике в любом месте окна браузера
    const target = e.target // находим элемент, на котором был кли
    if (!target.closest('.header__menu') && !target.closest('.header__burger')) { // если этот элемент или его родительские элементы не окно навигации и не кнопка
      header__burger.classList.remove('active');
      header_menu.classList.remove('active'); // то закрываем окно навигации, удаляя активный класс
    }
  })

})

$('input[name=phone]').mask("+7 (999) 999-99-99");
