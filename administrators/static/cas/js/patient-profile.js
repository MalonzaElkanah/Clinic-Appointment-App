/*
Author       : MalonzaElkanah
Template Name: Doccure - Patient-Profile
Version      : 1.0
*/

(function($) {
    "use strict";
	
	// Prescription Add More
	
    $(".prescription-info").on('click','.trash', function () {
		$(this).closest('.prescription-cont').remove();
		return false;
    });

    $(".add-prescription").on('click', function () {
		var form_num = parseInt($("input[name='form-num']").val());
		var num = form_num + 1;
		$("#form-num").attr('value', num);

		var content = '<tr class="prescription-cont">' +
			'<td> <input class="form-control" type="text" name="name_'+form_num+'"> </td>' +
			'<td> <input class="form-control" type="text" name="quantity_'+form_num+'"> </td>' +
			'<td> <input class="form-control" type="text" name="days_'+form_num+'"> </td>' +
			'<td>' +
				'<div class="form-check form-check-inline">' +
					'<label class="form-check-label">' +
						'<input class="form-check-input" type="checkbox" name="morning_'+form_num+'"> Morning' +
					'</label>' +
				'</div>' +
				'<div class="form-check form-check-inline">' +
					'<label class="form-check-label">' +
						'<input class="form-check-input" type="checkbox" name="afternoon_'+form_num+'"> Afternoon' +
					'</label>' +
				'</div>' +
				'<div class="form-check form-check-inline">' +
					'<label class="form-check-label">' +
						'<input class="form-check-input" type="checkbox"name="evening_'+form_num+'"> Evening' +
					'</label>' +
				'</div>' +
				'<div class="form-check form-check-inline">' +
					'<label class="form-check-label">' +
						'<input class="form-check-input" type="checkbox" name="night_'+form_num+'"> Night' +
					'</label>' +
				'</div>' +
			'</td>' +
			'<td>' +
				'<a href="#" class="btn bg-danger-light trash"><i class="far fa-trash-alt"></i></a>' +
			'</td>' +
		'</tr>';
		
        $(".prescription-info").append(content);
        return false;
    });
	
	// Experience Add More
	
    $(".bill-info").on('click','.trash', function () {
		$(this).closest('.bill-cont').remove();
		return false;
    });

    $(".add-bill").on('click', function () {
		var form_num = parseInt($("input[name='form-num']").val());
		var num = form_num + 1;
		$("#form-num").attr('value', num);
		var content = '<tr class="bill-cont">' +								
			'<td> <input type="text" class="form-control" name="title_'+form_num+'" required> </td>' +
			'<td> <input type="text" class="form-control" name="amount_'+form_num+'" required> </td>' +							
			'<td>' +
				'<a href="#" class="btn bg-danger-light trash"><i class="far fa-trash-alt"></i></a>' +															
			'</td>' +
		'</tr>';
		
        $(".bill-info").append(content);
        return false;
    });
	
	// Awards Add More
	
    $(".awards-info").on('click','.trash', function () {
		$(this).closest('.awards-cont').remove();
		return false;
    });

    $(".add-award").on('click', function () {

    	var form_num = parseInt($("input[name='awd_form-num']").val());
		var num = form_num + 1;
		$("#awd_form-num").attr('value', num);
        var regcontent = '<div class="row form-row awards-cont">' +
			'<div class="col-12 col-md-5">' +
				'<div class="form-group">' +
					'<label>Awards</label>' +
					'<input type="text" class="form-control" name="award-'+form_num+'" required>' +
				'</div>' +
			'</div>' +
			'<div class="col-12 col-md-5">' +
				'<div class="form-group">' +
					'<label>Year</label>' +
					'<input type="text" class="form-control datetimepicker" name="year-'+form_num+'" required>' +
				'</div>' +
			'</div>' +
			'<div class="col-12 col-md-2">' +
				'<label class="d-md-block d-sm-none d-none">&nbsp;</label>' +
				'<a href="#" class="btn btn-danger trash"><i class="far fa-trash-alt"></i></a>' +
			'</div>' +
		'</div>';
		
        $(".awards-info").append(regcontent);
        return false;
    });
	
	// Membership Add More
	
    $(".membership-info").on('click','.trash', function () {
		$(this).closest('.membership-cont').remove();
		return false;
    });

    $(".add-membership").on('click', function () {

    	/*var form_num = parseInt($("input[name='mbr_form-num']").val());
		var num = form_num + 1;
		alert(num);
		$("#mbr_form-num-id").val(''+num+'');*/
		var input_num = parseInt($("#mbr_count").text());
    	var membershipcontent = '<div class="row form-row membership-cont">' +
			'<div class="col-12 col-md-10 col-lg-5">' +
				'<div class="form-group">' +
					'<label>Memberships</label>' +
					'<input type="text" class="form-control" name="membership-'+input_num+'" required>' +
				'</div>' +
			'</div>' +
			'<div class="col-12 col-md-2 col-lg-2">' +
				'<label class="d-md-block d-sm-none d-none">&nbsp;</label>' +
				'<a href="#" class="btn btn-danger trash"><i class="far fa-trash-alt"></i></a>' +
			'</div>' +
		'</div>';
		
		input_num = input_num + 1;
    	$("#mbr_count").text(''+input_num+'');
    	$("#mbr_form-num-id").attr('value', input_num);

		
        $(".membership-info").append(membershipcontent);
        return false;
    });
	
	// Registration Add More
	
    $(".registrations-info").on('click','.trash', function () {
		$(this).closest('.reg-cont').remove();
		return false;
    });

    $(".add-reg").on('click', function () {

        var form_num = parseInt($("input[name='reg_form-num']").val());
		var num = form_num + 1;
		$("#reg_form-num").attr('value', num);
        var regcontent = '<div class="row form-row reg-cont">' +
			'<div class="col-12 col-md-5">' +
				'<div class="form-group">' +
					'<label>Registrations</label>' +
					'<input type="text" class="form-control" name="registration-'+form_num+'" required>' +
				'</div>' +
			'</div>' +
			'<div class="col-12 col-md-5">' +
				'<div class="form-group">' +
					'<label>Year</label>' +
					'<input type="text" class="form-control datetimepicker" name="year-'+form_num+'" required>' +
				'</div>' +
			'</div>' +
			'<div class="col-12 col-md-2">' +
				'<label class="d-md-block d-sm-none d-none">&nbsp;</label>' +
				'<a href="#" class="btn btn-danger trash"><i class="far fa-trash-alt"></i></a>' +
			'</div>' +
		'</div>';
		
        $(".registrations-info").append(regcontent);
        return false;
    });
	
})(jQuery);