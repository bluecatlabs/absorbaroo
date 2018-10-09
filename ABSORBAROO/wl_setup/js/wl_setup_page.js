// Copyright 2018 BlueCat Networks. All rights reserved.
// JavaScript for your page goes in here.
$(document).ready(function()
{

        $('#whitelisturl').focusout( function() {

		console.log ('inside js')
                wlurl = $('#whitelisturl').val()
                $.ajax({
                        type: 'POST',
                        url: '/wl_setup/validateurl',
			contentType: "application/json; charset=utf-8",
                        data: JSON.stringify({ 'url': wlurl }),
                        dataType:'json',
                        success: function (data) {
				if (data.status == "failure") {
					$('#whitelisturl').css('color', 'red')
					$('#submit').prop("disabled", true)
				} else {
					$('#whitelisturl').css('color', 'white')
					$('#submit').prop("disabled", false)
				}
                        },
			failure: function (data) {
				$('#whitelisturl').css('color', 'red')
				$('#submit').prop("disabled", true)
			}
                })
        })

        $('#interval').focusout( function() {
		$('#submit').prop("disabled", false)
	})
});

