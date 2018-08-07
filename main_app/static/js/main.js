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
});