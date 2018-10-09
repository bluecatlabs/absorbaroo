// Copyright 2018 BlueCat Networks. All rights reserved.
// JavaScript for your page goes in here.


$(document).ready(function()
{
        $('#key').focusout( function() {

                value = $('#key').val()
                $.ajax({
                        type: 'POST',
                        url: '/sdwan_setup/validatekey',
                        contentType: "application/json; charset=utf-8",
                        data: JSON.stringify({ 'key': value }),
                        dataType:'json',
                        success: function (data) {
                                if (data.status == "failure") {
                                        $('#key').css('color', 'red')
                                	$('#submit').prop("disabled", true)
                                } else {
                                        $('#key').css('color', 'white')
                                        $('#submit').prop("disabled", false)
                                }
                        },
                        failure: function (data) {
                                $('#key').css('color', 'red')
                                $('#submit').prop("disabled", true)
                        }
                })
        })

        $('#orgname').focusout( function() {

                key = $('#key').val()
                orgname = $('#orgname').val()
                $.ajax({
                        type: 'POST',
                        url: '/sdwan_setup/validateorgname',
                        contentType: "application/json; charset=utf-8",
                        data: JSON.stringify({ 'key': key, 'orgname': orgname }),
                        dataType:'json',
                        success: function (data) {
                                if (data.status == "failure") {
                                        $('#orgname').css('color', 'red')
                                        $('#submit').prop("disabled", true)
                                } else {
                                        $('#orgname').css('color', 'white')
                                        $('#submit').prop("disabled", false)
                                }
                        },
                        failure: function (data) {
                                $('#orgname').css('color', 'red')
                                $('#submit').prop("disabled", true)
                        }
                })
        })

        $('#templatename').focusout( function() {

                key = $('#key').val()
                orgname = $('#orgname').val()
                template = $('#templatename').val()
                $.ajax({
                        type: 'POST',
                        url: '/sdwan_setup/validatetemplate',
                        contentType: "application/json; charset=utf-8",
                        data: JSON.stringify({ 'key': key, 'orgname': orgname, 'template': template }),
                        dataType:'json',
                        success: function (data) {
                                if (data.status == "failure") {
                                        $('#templatename').css('color', 'red')
                                        $('#submit').prop("disabled", true)
                                } else {
                                        $('#templatename').css('color', 'white')
                                        $('#submit').prop("disabled", false)
                                }
                        },
                        failure: function (data) {
                                $('#templatename').css('color', 'red')
                                $('#submit').prop("disabled", true)
                        }
                })
        })

});

