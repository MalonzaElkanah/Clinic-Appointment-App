/*
Author       : Dreamguys
Template Name: Doccure - Bootstrap Template
Version      : 1.0
*/

(function($) {
    "use strict";
	
	// Stick Sidebar
	
	if ($(window).width() > 767) {
		if($('.theiaStickySidebar').length > 0) {
			$('.theiaStickySidebar').theiaStickySidebar({
			  // Settings
			  additionalMarginTop: 30
			});
		}
	}
	
// Sidebar
	if($(window).width() <= 991){
	var Sidemenu = function() {
		this.$menuItem = $('.main-nav a');
	};
	
	function init() {
		var $this = Sidemenu;
		$('.main-nav a').on('click', function(e) {
			if($(this).parent().hasClass('has-submenu')) {
				e.preventDefault();
			}
			if(!$(this).hasClass('submenu')) {
				$('ul', $(this).parents('ul:first')).slideUp(350);
				$('a', $(this).parents('ul:first')).removeClass('submenu');
				$(this).next('ul').slideDown(350);
				$(this).addClass('submenu');
			} else if($(this).hasClass('submenu')) {
				$(this).removeClass('submenu');
				$(this).next('ul').slideUp(350);
			}
		});
		//$('.main-nav li.has-submenu a.active').parents('li:last').children('a:first').addClass('active').trigger('click');
	}

	// Sidebar Initiate
	init();
	}
	
	// Textarea Text Count
	
	var maxLength = 100;
	$('#review_desc').on('keyup change', function () {
		var length = $(this).val().length;
		 length = maxLength-length;
		$('#chars').text(length);
	});
	
	// Select 2
	
	if($('.select').length > 0) {
		$('.select').select2({
			minimumResultsForSearch: -1,
			width: '100%'
		});
	}
	
	// Date Time Picker
	
	if($('.datetimepicker').length > 0) {
		$('.datetimepicker').datetimepicker({
			format: 'YYYY-MM-DD',
			icons: {
				up: "fas fa-chevron-up",
				down: "fas fa-chevron-down",
				next: 'fas fa-chevron-right',
				previous: 'fas fa-chevron-left'
			}
		});
	}
	
	// Fancybox Gallery
	
	if($('.clinic-gallery a').length > 0) {
		$('.clinic-gallery a').fancybox({
			buttons: [
				"thumbs",
				"close"
			],
		});	
	}
	
	// Floating Label

	if($('.floating').length > 0 ){
		$('.floating').on('focus blur', function (e) {
		$(this).parents('.form-focus').toggleClass('focused', (e.type === 'focus' || this.value.length > 0));
		}).trigger('blur');
	}
	
	// Mobile menu sidebar overlay
	
	$('body').append('<div class="sidebar-overlay"></div>');
	$(document).on('click', '#mobile_btn', function() {
		$('main-wrapper').toggleClass('slide-nav');
		$('.sidebar-overlay').toggleClass('opened');
		$('html').addClass('menu-opened');
		return false;
	});
	
	$(document).on('click', '.sidebar-overlay', function() {
		$('html').removeClass('menu-opened');
		$(this).removeClass('opened');
		$('main-wrapper').removeClass('slide-nav');
	});
	
	$(document).on('click', '#menu_close', function() {
		$('html').removeClass('menu-opened');
		$('.sidebar-overlay').removeClass('opened');
		$('main-wrapper').removeClass('slide-nav');
	});
	
	// Mobile Menu
	
	/*if($(window).width() <= 991){
		mobileSidebar();
	} else {
		$('html').removeClass('menu-opened');
	}*/
	
	/*function mobileSidebar() {
		$('.main-nav a').on('click', function(e) {
			$('.dropdown-menu').each(function() {
			  if($(this).hasClass('show')) {
				  $(this).slideUp(350);
			  }
			});
			if(!$(this).next('.dropdown-menu').hasClass('show')) {
				$(this).next('.dropdown-menu').slideDown(350);
			}
			
		});
	}*/
	
	// Tooltip
	
	if($('[data-toggle="tooltip"]').length > 0 ){
		$('[data-toggle="tooltip"]').tooltip();
	}
	
	// Add More Hours
	
    $(".hours-info").on('click','.trash', function () {
		$(this).closest('.hours-cont').remove();
		return false;
    });

    $(".add-hours").on('click', function () {
		var form_num = parseInt($("input[name='add_form-num']").val());

		var options = '<option value="">-</option>' +
		'<option value="00:00:00">12.00 AM</option>'+
		'<option value="00:30:00">12.30 AM</option>'+
		'<option value="01:00:00">01.00 AM</option>'+
		'<option value="01:30:00">01.30 AM</option>'+
		'<option value="02:00:00">02.00 AM</option>'+
		'<option value="02:30:00">02.30 AM</option>'+
		'<option value="03:00:00">03.00 AM</option>'+
		'<option value="03:30:00">03.30 AM</option>'+
		'<option value="04:00:00">04.00 AM</option>'+
		'<option value="04:30:00">04.30 AM</option>'+
		'<option value="05:00:00">05.00 AM</option>'+
		'<option value="05:30:00">05.30 AM</option>'+
		'<option value="06:00:00">06.00 AM</option>'+
		'<option value="06:30:00">06.30 AM</option>'+
		'<option value="07:00:00">07.00 AM</option>'+
		'<option value="07:30:00">07.30 AM</option>'+
		'<option value="08:00:00">08.00 AM</option>'+
		'<option value="08:30:00">08.30 AM</option>'+
		'<option value="09:00:00">09.00 AM</option>'+
		'<option value="09:30:00">09.30 AM</option>'+
		'<option value="10:00:00">10.00 AM</option>'+
		'<option value="10:30:00">10.30 AM</option>'+
		'<option value="11:00:00">11.00 AM</option>'+
		'<option value="11:30:00">11.30 AM</option>'+
		'<option value="12:00:00">12.00 PM</option>'+
		'<option value="12:30:00">12.30 PM</option>'+
		'<option value="13:00:00">01.00 PM</option>'+
		'<option value="13:30:00">01.30 PM</option>'+
		'<option value="14:00:00">02.00 PM</option>'+
		'<option value="14:30:00">02.30 PM</option>'+
		'<option value="15:00:00">03.00 PM</option>'+
		'<option value="15:30:00">03.30 PM</option>'+
		'<option value="16:00:00">04.00 PM</option>'+
		'<option value="16:30:00">04.30 PM</option>'+
		'<option value="17:00:00">05.00 PM</option>'+
		'<option value="17:30:00">05.30 PM</option>'+
		'<option value="18:00:00">06.00 PM</option>'+
		'<option value="18:30:00">06.30 PM</option>'+
		'<option value="19:00:00">07.00 PM</option>'+
		'<option value="19:30:00">07.30 PM</option>'+
		'<option value="20:00:00">08.00 PM</option>'+
		'<option value="20:30:00">08.30 PM</option>'+
		'<option value="21:00:00">09.00 PM</option>'+
		'<option value="21:30:00">09.30 PM</option>'+
		'<option value="22:00:00">10.00 PM</option>'+
		'<option value="22:30:00">10.30 PM</option>'+
		'<option value="23:00:00">11.00 PM</option>'+
		'<option value="23:30:00">11.30 PM</option>';

		var hourscontent = '<div class="row form-row hours-cont">' +
			'<div class="col-12 col-md-10">' +
				'<div class="row form-row">' +
					'<div class="col-12 col-md-6">' +
						'<div class="form-group">' +
							'<label>Start Time</label>' +
							'<select class="form-control" name="start_time_'+form_num+'">' +
								''+options+''+
							'</select>' +
						'</div>' +
					'</div>' +
					'<div class="col-12 col-md-6">' +
						'<div class="form-group">' +
							'<label>End Time</label>' +
							'<select class="form-control" name="end_time_'+form_num+'">' +
								''+options+''+
							'</select>' +
						'</div>' +
					'</div>' +
				'</div>' +
			'</div>' +
			'<div class="col-12 col-md-2"><label class="d-md-block d-sm-none d-none">&nbsp;</label><a href="#" class="btn btn-danger trash"><i class="far fa-trash-alt"></i></a></div>' +
		'</div>';
		
        $(".hours-info").append(hourscontent);
        var num = form_num + 1;
		$("input[name='add_form-num']").attr('value', num);
    });

	$(".edit-hours").on('click', function () {
		var form_num = parseInt($("input[name='edit_form-num']").val());

		var options = '<option value="">-</option>' +
		'<option value="00:00:00">12.00 AM</option>'+
		'<option value="00:30:00">12.30 AM</option>'+
		'<option value="01:00:00">01.00 AM</option>'+
		'<option value="01:30:00">01.30 AM</option>'+
		'<option value="02:00:00">02.00 AM</option>'+
		'<option value="02:30:00">02.30 AM</option>'+
		'<option value="03:00:00">03.00 AM</option>'+
		'<option value="03:30:00">03.30 AM</option>'+
		'<option value="04:00:00">04.00 AM</option>'+
		'<option value="04:30:00">04.30 AM</option>'+
		'<option value="05:00:00">05.00 AM</option>'+
		'<option value="05:30:00">05.30 AM</option>'+
		'<option value="06:00:00">06.00 AM</option>'+
		'<option value="06:30:00">06.30 AM</option>'+
		'<option value="07:00:00">07.00 AM</option>'+
		'<option value="07:30:00">07.30 AM</option>'+
		'<option value="08:00:00">08.00 AM</option>'+
		'<option value="08:30:00">08.30 AM</option>'+
		'<option value="09:00:00">09.00 AM</option>'+
		'<option value="09:30:00">09.30 AM</option>'+
		'<option value="10:00:00">10.00 AM</option>'+
		'<option value="10:30:00">10.30 AM</option>'+
		'<option value="11:00:00">11.00 AM</option>'+
		'<option value="11:30:00">11.30 AM</option>'+
		'<option value="12:00:00">12.00 PM</option>'+
		'<option value="12:30:00">12.30 PM</option>'+
		'<option value="13:00:00">01.00 PM</option>'+
		'<option value="13:30:00">01.30 PM</option>'+
		'<option value="14:00:00">02.00 PM</option>'+
		'<option value="14:30:00">02.30 PM</option>'+
		'<option value="15:00:00">03.00 PM</option>'+
		'<option value="15:30:00">03.30 PM</option>'+
		'<option value="16:00:00">04.00 PM</option>'+
		'<option value="16:30:00">04.30 PM</option>'+
		'<option value="17:00:00">05.00 PM</option>'+
		'<option value="17:30:00">05.30 PM</option>'+
		'<option value="18:00:00">06.00 PM</option>'+
		'<option value="18:30:00">06.30 PM</option>'+
		'<option value="19:00:00">07.00 PM</option>'+
		'<option value="19:30:00">07.30 PM</option>'+
		'<option value="20:00:00">08.00 PM</option>'+
		'<option value="20:30:00">08.30 PM</option>'+
		'<option value="21:00:00">09.00 PM</option>'+
		'<option value="21:30:00">09.30 PM</option>'+
		'<option value="22:00:00">10.00 PM</option>'+
		'<option value="22:30:00">10.30 PM</option>'+
		'<option value="23:00:00">11.00 PM</option>'+
		'<option value="23:30:00">11.30 PM</option>';

		var hourscontent = '<div class="row form-row hours-cont">' +
			'<div class="col-12 col-md-10">' +
				'<div class="row form-row">' +
					'<div class="col-12 col-md-6">' +
						'<div class="form-group">' +
							'<label>Start Time</label>' +
							'<select class="form-control" name="start_time_'+form_num+'">' +
								''+options+''+
							'</select>' +
						'</div>' +
					'</div>' +
					'<div class="col-12 col-md-6">' +
						'<div class="form-group">' +
							'<label>End Time</label>' +
							'<select class="form-control" name="end_time_'+form_num+'">' +
								''+options+''+
							'</select>' +
						'</div>' +
					'</div>' +
				'</div>' +
			'</div>' +
			'<div class="col-12 col-md-2"><label class="d-md-block d-sm-none d-none">&nbsp;</label><a href="#" class="btn btn-danger trash"><i class="far fa-trash-alt"></i></a></div>' +
		'</div>';
		
        $(".edit_hours-info").append(hourscontent);
        var num = form_num + 1;
		$("input[name='edit_form-num']").attr('value', num);
    });
	
	// Content div min height set
	
	function resizeInnerDiv() {
		var height = $(window).height();	
		var header_height = $(".header").height();
		var footer_height = $(".footer").height();
		var setheight = height - header_height;
		var trueheight = setheight - footer_height;
		$(".content").css("min-height", trueheight);
	}
	
	if($('.content').length > 0 ){
		resizeInnerDiv();
	}

	$(window).resize(function(){
		if($('.content').length > 0 ){
			resizeInnerDiv();
		}
		/*if($(window).width() <= 991){
			mobileSidebar();
		} else {
			$('html').removeClass('menu-opened');
		}*/
	});
	
	// Slick Slider
	
	if($('.specialities-slider').length > 0) {
		$('.specialities-slider').slick({
			dots: true,
			autoplay:false,
			infinite: true,
			variableWidth: true,
			prevArrow: false,
			nextArrow: false
		});
	}
	
	if($('.doctor-slider').length > 0) {
		$('.doctor-slider').slick({
			dots: false,
			autoplay:false,
			infinite: true,
			variableWidth: true,
		});
	}
	if($('.features-slider').length > 0) {
		$('.features-slider').slick({
			dots: true,
			infinite: true,
			centerMode: true,
			slidesToShow: 3,
			speed: 500,
			variableWidth: true,
			arrows: false,
			autoplay:false,
			responsive: [{
				  breakpoint: 992,
				  settings: {
					slidesToShow: 1
				  }

			}]
		});
	}
	
	// Date Time Picker
	
	if($('.datepicker').length > 0) {
		$('.datepicker').datetimepicker({
			viewMode: 'years',
			showTodayButton: true,
			format: 'YYYY-MM-DD',
			// minDate:new Date(),
			widgetPositioning:{
				horizontal: 'auto',	
				vertical: 'bottom'
			}
		});
	}
	
	// Chat

	var chatAppTarget = $('.chat-window');
	(function() {
		if ($(window).width() > 991)
			chatAppTarget.removeClass('chat-slide');
		
		$(document).on("click",".chat-window .chat-users-list a.media",function () {
			if ($(window).width() <= 991) {
				chatAppTarget.addClass('chat-slide');
			}
			return false;
		});
		$(document).on("click","#back_user_list",function () {
			if ($(window).width() <= 991) {
				chatAppTarget.removeClass('chat-slide');
			}	
			return false;
		});
	})();
	
	// Circle Progress Bar
	
	function animateElements() {
		$('.circle-bar1').each(function () {
			var elementPos = $(this).offset().top;
			var topOfWindow = $(window).scrollTop();
			var percent = $(this).find('.circle-graph1').attr('data-percent');
			var animate = $(this).data('animate');
			if (elementPos < topOfWindow + $(window).height() - 30 && !animate) {
				$(this).data('animate', true);
				$(this).find('.circle-graph1').circleProgress({
					value: percent / 100,
					size : 400,
					thickness: 30,
					fill: {
						color: '#da3f81'
					}
				});
			}
		});
		$('.circle-bar2').each(function () {
			var elementPos = $(this).offset().top;
			var topOfWindow = $(window).scrollTop();
			var percent = $(this).find('.circle-graph2').attr('data-percent');
			var animate = $(this).data('animate');
			if (elementPos < topOfWindow + $(window).height() - 30 && !animate) {
				$(this).data('animate', true);
				$(this).find('.circle-graph2').circleProgress({
					value: percent / 100,
					size : 400,
					thickness: 30,
					fill: {
						color: '#68dda9'
					}
				});
			}
		});
		$('.circle-bar3').each(function () {
			var elementPos = $(this).offset().top;
			var topOfWindow = $(window).scrollTop();
			var percent = $(this).find('.circle-graph3').attr('data-percent');
			var animate = $(this).data('animate');
			if (elementPos < topOfWindow + $(window).height() - 30 && !animate) {
				$(this).data('animate', true);
				$(this).find('.circle-graph3').circleProgress({
					value: percent / 100,
					size : 400,
					thickness: 30,
					fill: {
						color: '#1b5a90'
					}
				});
			}
		});
	}	
	
	if($('.circle-bar').length > 0) {
		animateElements();
	}
	$(window).scroll(animateElements);
	
})(jQuery);