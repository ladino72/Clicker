$(document).ready(function() {

	$('#end_test').on('submit', function(event) {

		$.fn.myFunction = function(){
		    return $("#formCheck-3").is(':checked');

    }
		$.ajax({
			data : {
				ischecked : $.fn.myFunction()
			},
			type : 'POST',
			url : "/end_test"
		})
		.done(function(data) {

				$('#successAlert').text(data.message).show();
				setTimeout('$("#successAlert").hide()',4500);

				if (data.enable === 'Yes'){
					$('#formCheck-4').prop("disabled", false);
					$('#grade_btn').prop("disabled", false);

				}
				if (data.enable === 'No'){
					$('#formCheck-4').prop("disabled", true);
					$('#grade_btn').prop("disabled", true);

				}

		});

		event.preventDefault();

	});

});