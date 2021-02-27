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
	            console.log(response);
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
})(jQuery);