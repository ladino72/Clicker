$(document).ready(function() {

	$('#enable_test').on('submit', function(event) {

		$.fn.myFunction = function(){
		    return $("#formCheck-1").is(':checked');

    }
		$.ajax({
			data : {
				ischecked : $.fn.myFunction()
			},
			type : 'POST',
			url : "/enable_test"
		})
		.done(function(data) {

				$('#successAlert').text(data.message).show();
				setTimeout('$("#successAlert").hide()',4500);

				if (data.enable === 'Yes'){
					$('#formCheck-3').prop("disabled", false);
					$('#end_test_btn').prop("disabled", false);

				}
				if (data.enable === 'No'){
					$('#formCheck-3').prop("disabled", true);
					$('#formCheck-3').prop("checked", false);
					$('#end_test_btn').prop("disabled", true);
				}

		});

		event.preventDefault();

	});

});