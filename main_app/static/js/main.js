$(document).ready(function() {
	console.log('DOC REACY');

	$('.category-filters button').click(function() {
		if($(this).is('.filter-active')) {
			$(this).removeClass('filter-active');
		}
		else {
			$(this).addClass('filter-active');
		}
	});
});