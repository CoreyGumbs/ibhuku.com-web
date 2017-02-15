$(document).ready(function(){
	
	//closes message framework after user action
	setTimeout(function(){
		$('.ibk-messages').animate({
			height: 'toggle',
			opacity: '0'
		});
	}, 2000);

});