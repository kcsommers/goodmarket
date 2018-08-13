$(document).ready(function() {
	console.log('DOC READY');
	
	$('.category-filters button').click(function() {
		let category = $(this).attr('data-id');
		$('.filter-active').removeClass('filter-active');

		if($(this).is('.filter-active')) {
			if($(this).is('.show-all')) {
				$('.market-item').addClass('filtered');
			}
			else {
				$(this).addClass('filtered');
			}
		}
		else {
			if($(this).is('.show-all')) {
				$('.market-item').removeClass('filtered');
			}
			else {
				$('.market-item').addClass('filtered');
				$(`.${category}`).removeClass('filtered');
			}
		}
		$(this).addClass('filter-active');
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

	$('.sell-form-categories button').click(function(e) {
		e.preventDefault();
		$('.sell-form-categories button.active').removeClass('active');
		$(this).addClass('active');
		let value = $(this).attr('id');
		$('.category-hidden').val(value);
	});

	$('.char-img').click(function(e) {
		e.preventDefault();
		$('.char-selected').removeClass('char-selected');
		$(this).addClass('char-selected');
		let value = $(this).attr('id');
		console.log(value)
		$('.charity-hidden').val(value);
		console.log($('.charity-hidden').val())
	});

	$('.sell-form-percentage button').click(function(e) {
		e.preventDefault();
		$('.sell-form-percentage button.active').removeClass('active');
		$(this).addClass('active');
		let value = $(this).attr('id');
		$('.charity-percent-hidden').val(value);
	});
});

function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}