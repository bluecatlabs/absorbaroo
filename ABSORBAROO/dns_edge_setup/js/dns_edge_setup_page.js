// Copyright 2018 BlueCat Networks. All rights reserved.
// JavaScript for your page goes in here.

$(document).ready(function()
{
    	$("#edgepassword").prop("disabled", false);

        $('#edgeurl').focusout( function() {
                console.log ('inside js')
                edgeurl = $('#edgeurl').val()
                $.ajax({
                        type: 'POST',
                        url: '/dns_edge_setup/validateurl',
                        contentType: "application/json; charset=utf-8",
                        data: JSON.stringify({ 'url': edgeurl }),
                        dataType:'json',
                        success: function (data) {
                                if (data.status == "failure") {
                                        $('#edgeurl').css('color', 'red')
                                        $('#submit').prop("disabled", true)
                                } else {
                                        $('#edgeurl').css('color', 'white')
                                        $('#submit').prop("disabled", false)
                                }
                        },
                        failure: function (data) {
                                $('#edgeurl').css('color', 'red')
                                $('#submit').prop("disabled", true)
                        }
                })
        })

        $('#edgepassword').focusout( function() {
                console.log ('inside js')
                edgeurl = $('#edgeurl').val()
                edgeusername = $('#edgeusername').val()
                edgepassword = $('#edgepassword').val()
                $.ajax({
                        type: 'POST',
                        url: '/dns_edge_setup/validateauth',
                        contentType: "application/json; charset=utf-8",
                        data: JSON.stringify({ 'url': edgeurl, 'username': edgeusername, 'password': edgepassword }),
                        dataType:'json',
                        success: function (data) {
                                if (data.status == "failure") {
                                        $('#edgeusername').css('color', 'red')
                                        $('#edgepassword').css('color', 'red')
                                        $('#submit').prop("disabled", true)
                                } else {
                                        $('#edgeusername').css('color', 'white')
                                        $('#edgepassword').css('color', 'white')
                                        $('#submit').prop("disabled", false)
                                }
                        },
                        failure: function (data) {
                                $('#edgeusername').css('color', 'red')
                                $('#edgepassword').css('color', 'red')
                                $('#submit').prop("disabled", true)
                        }
                })
        })

        $('#dlname').focusout( function() {
                console.log ('inside js')
                edgeurl = $('#edgeurl').val()
                edgeusername = $('#edgeusername').val()
                edgepassword = $('#edgepassword').val()
                dlname = $('#dlname').val()

                $.ajax({
                        type: 'POST',
                        url: '/dns_edge_setup/validatedlname',
                        contentType: "application/json; charset=utf-8",
                        data: JSON.stringify({ 'url': edgeurl, 'username': edgeusername, 'password': edgepassword, 'dlname': dlname }),
                        dataType:'json',
                        success: function (data) {
                                if (data.status == "failure") {
                                        $('#dlname').css('color', 'red')
                                        $('#submit').prop("disabled", true)
                                } else {
                                        $('#dlname').css('color', 'white')
                                        $('#submit').prop("disabled", false)
                                }
                        },
                        failure: function (data) {
                                $('#dlname').css('color', 'red')
                                $('#submit').prop("disabled", true)
                        }
                })
        })

});


