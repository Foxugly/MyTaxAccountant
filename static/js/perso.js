/**
 * Created by renaud on 03/02/16.
 */

$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});


$(document).ready(function() {

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $(function () {
        'use strict';
        var url = '/upload/basic/';
        var csrftoken = $.cookie('csrftoken');
        $('#fileupload').fileupload({
            url: url,
            crossDomain: false,
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            dataType: 'json',
            done: function (e, data) {
                $("#fileupload_list" ).removeClass( "hide" );
                $.each(data.result.files, function (index, file) {
                    $("#files-group").append('\n<li class="list-group-item list-group-item-success"><span>' + file.name + '</span><button id="' + file.id + '" type="button" class="close close_fileupload">&times;</button></li>\n');
                });
                $(".close_fileupload").click(function(){
                    close_uploadfile($(this));
                });
            },
            progressall: function (e, data) {
                $("#progress_row" ).removeClass( "hide" );
                var progress = parseInt(data.loaded / data.total * 100, 10);
                $('#progress .progress-bar').css(
                    'width',
                    progress + '%'
                );
                if (progress == 100){
                    $("#progress_row" ).addClass( "hide" );
                }
            }
        }).prop('disabled', !$.support.fileInput)
            .parent().addClass($.support.fileInput ? undefined : 'disabled');
    });


    $('#confirm_yes_close').click(function(){
        $('#confirm_yes').hide();
    });

    $('#confirm_yes_ok').click(function(){
        $('#confirm_yes').hide();
    });

    $('#confirm_no_close').click(function(){
        $('#confirm_no').hide();
    });

    $('#confirm_no_ok').click(function(){
        $('#confirm_no').hide();
    });

    $('#language').change(function() {
        console.log("LANGUAGE");
        var select = $(this);
        var mydata = {lang:select.val()};
        var url = '/lang/';
        $.ajax({
            url: url,
            type: 'POST',
            data: mydata,
            traditional: true,
            dataType: 'json',
            success: function(result){
                if (result['return']){
                    location.reload();
                }
                else{
                    $('#confirm_no_error').val(result['errors']);
                    $('#confirm_no').show();
                }
            }
        });
    });

    function update_trimesters(){
        var y = $('#sel_year').val();
        var url = '/year/' + y + '/list/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                $('#sel_trimester').empty().append('<optgroup label = "Choose a trimester">')
                for( var i = 0, len = result.length; i < len; i++ ) {
                    $('#sel_trimester').append('<option value="'+ result[i].id + '">'+ result[i].name +'</option>')
                }
                $('#sel_trimester').append('</optgroup>');
                update_data();
            }
        });
    }

    function update_years(){
        var c = $('#sel_company').val();
        var url = '/company/' + c + '/list/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                $('#sel_year').empty().append('<optgroup label = "Choose a tax year">')
                for( var i = 0, len = result.length; i < len; i++ ) {
                    $('#sel_year').append('<option value="'+ result[i].id + '">'+ result[i].name +'</option>')
                }
                $('#sel_year').append('</optgroup>');
                update_trimesters();
            }
        });
    }

    $('#sel_trimester').change(function() {
        update_data();

    });
    $('#sel_year').change(function() {
        update_trimesters();

    });
    $('#sel_company').change(function() {
        update_years();
    });

    function close_uploadfile(e){
        var id = e.attr('id');
        var url = '/upload/remove/' + id + '/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
            }
        });
        e.parent().remove();
        if ($("#files-group li").length == 0){
            $("#fileupload_list" ).addClass( "hide" );
        }
    }

    function img_modal(e){
        var id = e.attr('id');
        var url = '/document/' + id + '/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                $("#modal-title").text(result['name']);
                $("#modal-body").html(result['img']);
            }
        });
    }

    function update_datatable(data){
        $('#datatable').dataTable().fnAddData([ data['id'], "<a id='" + data['id'] + "' class='img_modal' data-toggle='modal' data-target='#myModal'>" + data['name'] + "</a>", data['date'], data['description'], data['complete']]);
    }

    function save_form(){
        var form = $('#div_form form');
        var id = $('#doc_id').val();
        var url = '/document/' + id + '/update/';
        $.ajax({
            url: url,
            type: 'GET',
            data: form.serialize(),
            traditional: true,
            dataType: 'json',
            success: function(result){
                $('#alert_save_saved').show().delay( 1000 ).fadeOut(1000);
            }
        });
    }

    function view_form(valid, img, form,doc_id){
        if (valid == true){
            $('#div_img').html(img);
            $('#div_form').html('<input id="doc_id" type="hidden" name="doc_id" value="' + doc_id + '">' +form);
            $('#btn_save').click(function(){
                save_form();
            });
            $('#pagination').show();
        }
        else{
            $('#div_img').html(" ");
            $('#div_form').html('<div class="alert alert-info" role="alert">No documents for this category</div>');
            $('#pagination').hide();
        }
    }

    function update_data(){
        var t = $('#sel_trimester').val();
        var url = '/trimester/' + t + '/list_categories/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                for (i = 0; i < result['nav_list'].length; i++) {
                    var a = '<a data-target="#" data-toggle="pill" id="' + result['nav_list'][i]['id'] + '" href="#">' + result['nav_list'][i]['name'] + ' <span class="badge">'+ result['nav_list'][i]['n'] +'</span></a>';
                    $("ul.nav-pills li:eq(" + i + ") a").html(result['nav_list'][i]['name'] + ' <span class="badge">'+ result['nav_list'][i]['n'] +'</span>');
                    $("ul.nav-pills li:eq(" + i + ") a").attr("id",result['nav_list'][i]['id']);
                    $("ul.nav.nav-pills li:eq(" + i + ")").removeClass("active");
                }
                $("ul.nav.nav-pills li:eq(0)").addClass("active");
                $('#datatable').dataTable().fnClearTable();
                for (i = 0; i < result['doc_list'].length; i++) {
                    update_datatable(result['doc_list'][i]);
                    $(".img_modal").click(function(){
                        img_modal($(this));
                    });
                }
                $('#pagination').bootpag({total: result['nav_list'][0]['n'], page: 1});
                view_form(result['valid'], result['img'],result['form'], result['doc_id']);
            }
        });
    }


    function get_form_data(i){
        var id = $('ul.nav-pills li.active a').attr("id")
        var url = '/category/' + id + '/form/' + i + '/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                view_form(result['valid'], result['img'],result['form'], result['doc_id']);
            }
        });
    }


    $('#valid_files').click(function() {
        var files = []
        $('#files-group').find('li').each(function(){
            var current = $(this).find('span');
            files.push(current.text());
        });
        $('#files-group').empty()
        $("#fileupload_list" ).addClass( "hide" ); // TODO .hide();
        var jsonText = JSON.stringify(files);
        var id = $('ul.nav-pills li.active a').attr("id")
        var url = '/category/' + id + '/add_documents/';
        $.ajax({
            url: url,
            type: 'GET',
            data: {'files':files},
            traditional: true,
            dataType: 'html',
            success: function(result){
                result = JSON.parse(result);
                $('#datatable').dataTable().fnClearTable();
                for (i = 0; i < result['doc_list'].length; i++) {
                    update_datatable(result['doc_list'][i]);
                    $(".img_modal").click(function(){
                        img_modal($(this));
                    });
                }
                $('ul.nav-pills li.active span').html(result['n']);
            }
        });
    });

    $('ul.nav-pills li a').click(function (e) {
        $('ul.nav-pills li.active').removeClass('active')
        $(this).parent('li').addClass('active')
        var id = $('ul.nav-pills li.active a').attr("id")
        var url = '/category/' + id + '/list_documents/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                $('#datatable').dataTable().fnClearTable();
                for (i = 0; i < result['doc_list'].length; i++) {
                    update_datatable(result['doc_list'][i]);
                    $(".img_modal").click(function(){
                        img_modal($(this));
                    });
                }
                var n = parseInt(result['n']);
                $('#pagination').bootpag({total: n,page: 1}).on("page", function(event, num){
                    get_form_data(num);
                });
                get_form_data(1);
            }
        });
    });

    $(".img_modal").click(function(){
        img_modal($(this));
    });

    $("#view_group :input:radio").change(function() {
        var view = this.value;
        if (view == 'list'){
            $("#div_list").show();
            $("#div_img_form").hide();
            $('#alert_save_saved').hide();
        }
        else if (view == 'form'){
            $("#div_list").hide();
            $("#div_img_form").show();
            $('#alert_save_saved').hide();
            get_form_data(1);
        }
    });

    $('#pagination').bootpag({
            total: 1,
            page: 1,
            maxVisible: 5,
            leaps: true,
            firstLastUse: true,
            first: '←',
            last: '→',
            wrapClass: 'pagination',
            activeClass: 'active',
            disabledClass: 'disabled',
            nextClass: 'next',
            prevClass: 'prev',
            lastClass: 'last',
            firstClass: 'first'
        }).on("page", function(event, num){
            get_form_data(num);
    });
});
