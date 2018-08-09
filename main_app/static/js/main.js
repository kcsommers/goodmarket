$(document).ready(function() {
	console.log('DOC READY');
	
	$('.category-filters button').click(function() {
		let category = $(this).attr('data-id');
		if($(this).is('.filter-active')) {
			$(this).removeClass('filter-active');
			$(`.${category}`).removeClass('unfiltered');
		}
		else {
			$(this).addClass('filter-active');
			$(`.${category}`).removeClass('filter').addClass('unfiltered');
			$(`.market-item:not(.${category}, .unfiltered)`).addClass('filter');
		}
	});

	$('.sell-page-arrow-right').click(function() {
		if(!($('.sell-form-current').is('#sell-form-last'))) {
			$('.sell-form-current').removeClass('sell-form-current')
			.next().addClass('sell-form-current');
			$('.sell-form-container').animate({
				left: '-=100%'
			}, 500);
		}
	});

	$('.sell-page-arrow-left').click(function() {
		if(!($('.sell-form-current').is('#sell-form-first'))) {
			$('.sell-form-current').removeClass('sell-form-current')
			.prev().addClass('sell-form-current');
			$('.sell-form-container').animate({
				left: '+=100%'
			}, 500);
		}
	});

	$('.sell-form-category button').click(function(e) {
		e.preventDefault();
		let value = $(this).attr('id');
		$('.category-hidden').val(value);
	});

	$('.sell-form-charity-percent button').click(function(e) {
		e.preventDefault();
		let value = $(this).attr('id');
		$('.charity-percent-hidden').val(value);
	});
});