$(document).ready(function() {

	$('#new_test').on('submit', function(event) {

		$.fn.myFunction = function(){
		    return $("#formCheck-7").is(':checked');

    }
		$.ajax({
			data : {
				ischecked : $.fn.myFunction()
			},
			type : 'POST',
			url : "/new_test"
		})
		.done(function(data) {

				$('#successAlert').text(data.message).show();
				setTimeout('$("#successAlert").hide()',4500);

				if (data.enable === 'Yes'){
					$('#formCheck-1').prop("disabled", false);
					$('#formCheck-1').prop("checked", false);
					$('#enable_test_btn').prop("disabled", false);

					$('#formCheck-2').prop("disabled", true);
					$('#formCheck-2').prop("checked", false);
					$('#auth_see_sol_btn').prop("disabled", true);

					$('#formCheck-3').prop("disabled", true);
					$('#formCheck-3').prop("checked", false);
					$('#end_test_btn').prop("disabled", true);


					$('#grade_btn').prop("disabled", true);


					$('#show_stat_btn').prop("disabled", true);


					$('#save_results_btn').prop("disabled", true);

					$('#testbank_btn').prop("disabled", false);



				}
				if (data.enable === 'No'){
					$('#formCheck-1').prop("disabled", true);
					$('#formCheck-1').prop("checked", false);
					$('#enable_test_btn').prop("disabled", true);

					$('#formCheck-2').prop("disabled", true);
					$('#formCheck-2').prop("checked", false);
					$('#auth_see_sol_btn').prop("disabled", true);

					$('#formCheck-3').prop("disabled", true);
					$('#formCheck-3').prop("checked", false);
					$('#end_test_btn').prop("disabled", true);


					$('#grade_btn').prop("disabled", true);


					$('#show_stat_btn').prop("disabled", true);

					
					$('#save_results_btn').prop("disabled", true);
					$('#testbank_btn').prop("disabled", true);

				}

		});

		event.preventDefault();

	});

});