(function($) {
	"use strict";
	//submit form .add-form
	$(".add-form").submit(function(event) {
		event.preventDefault();
       	$.ajax({ 
       		data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: function(response) {
	            //console.log(response);
	            if(response['success']) {
	            	alert(response['success']);
		            //$("#feedbackmessage").html("<div class='alert alert-success'>Succesfully sent feedback, thank you!</div>");
		            //$("#feedbackform").addClass("hidden");
		            if(response['redirect']){
		            	window.location.href = response['redirect'];
		            }
	            }
	            if(response['error']) {
	            	alert(response['error']);
	            	//$("#id_error-text").html("Error: "+response['error']+"");
	            }
        	},
	        error: function (request, status, error) {
	            console.log(request.responseText);
	        }
       	});

	});

	$('.fav-btn').click(function(event){
		event.preventDefault();
		var p_data = {
			href: 1,
		};
		var serializedData = $(this).serialize();

		$.ajax({
            type: 'GET',
            url: $(this).attr('href'),
            data: serializedData,
            success: function (response) {
		        alert(response["responseJSON"]);	
            },
            error: function (response) {
                // alert the error if any error occured
                alert(response);
            }
        })
	});

	$('.ajax-link').click(function(event){
		event.preventDefault();
		var p_data = {
			href: 1,
		};
		var serializedData = $(this).serialize();

		$.ajax({
            type: 'GET',
            url: $(this).attr('href'),
            data: serializedData,
            success: function (response) {
		        if(response['success']) {
	            	alert(response['success']);
		            if(response['redirect']){
		            	window.location.href = response['redirect'];
		            }
	            }
	            if(response['error']) {
	            	alert(response['error']);
	            }
            },
            error: function (response) {
                alert(response);
            }
        })
	});


})(jQuery);