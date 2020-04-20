// Copyright 2020 BlueCat Networks (USA) Inc. and its affiliates
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// By: BlueCat Networks
// Date: 2019-08-28
// Gateway Version: 19.5.1
// Description: Absorbaroo V2 JS
var colModel = []

function load_col_model() {
    $.ajax({
        type: 'GET',
        url: '/absorbaroo/load_col_model',
        async: false
    })
    .done(function(data) {
        for (var i in data) {
            colModel.push(data[i]);
        }
    })
    .fail(function() {
        alert('Failed to fetch servers.');
    })
}

function update_service_areas() {
    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: '/absorbaroo/submit_service_areas',
        data: JSON.stringify($('#table').getRowData()),
        dataType: "json"
    });
}

$(document).ready(function()
{
    var grid = $('#table');

    load_col_model();

    grid.jqGrid({
        url: '/absorbaroo/load_service_areas',
        datatype: 'json',
        colModel: colModel,
        height: 'auto',
        pager : '#pager',
        scroll: true,
        caption: 'Service Areas'
    });

    $('#edge_key_file').on('change', function(event)
    {
        var key_file = document.getElementById('edge_key_file');
        var file = key_file.files[0];

        var reader = new FileReader();
        reader.addEventListener('load', update_client_key, false);
        reader.readAsText(file)

        function update_client_key(event){
            var access_key = JSON.parse(event.target.result);
            document.getElementById('edge_client_id').value = access_key.clientId;
            document.getElementById('edge_secret').value = access_key.clientSecret;
        }
    });

    $('#myTab a').click(function(e) {
      e.preventDefault();
      $(this).tab('show');
    });

    // store the currently selected tab in the hash value
    $("ul.nav-tabs > li > a").on("shown.bs.tab", function(e) {
      var id = $(e.target).attr("href").substr(1);
      window.location.hash = id;
    });

    // on load of the page: switch to the currently selected tab
    var hash = window.location.hash;
    $('#myTab a[href="' + hash + '"]').tab('show');


    $('#submit').on('click', function(e)
    {
        update_service_areas();
    });

    $('#execute_now').on('click', function(e)
    {
        update_service_areas();
    });

    $('#clear').on('click', function(e)
    {
        update_service_areas();
    });

    $('#cancel').on('click', function(e) {
        location.reload(true);
    });
});
