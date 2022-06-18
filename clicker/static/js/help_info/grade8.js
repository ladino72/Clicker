$(document).ready(function() {

	$('#grade').on('submit', function(event) {

		$.ajax({
			data : {

			},
			type : 'POST',
			url : "/grade"
		})
		.done(function(data) {

				$('#successAlert').text(data.message).show();
				setTimeout('$("#successAlert").hide()',4500);

				if (data.enable === 'enable_btns'){
					$('#show_stat_chk').removeAttr('disabled');
					$('#show_stat_btn').removeAttr('disabled');
					$('#save_results_chk').removeAttr('disabled');
					$('#save_results_btn').removeAttr('disabled');
					$('#formCheck-2').removeAttr('disabled');
					$('#auth_see_sol_btn').removeAttr('disabled');

				}

		});

		event.preventDefault();

	});

});