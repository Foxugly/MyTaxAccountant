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

    $('.select2').select2({width: 'resolve'});

    $('.select2-nosearch').select2({ width: 'resolve', minimumResultsForSearch: -1});

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
                for( var i = 0; i < result.length; i++ ) {
                    $('#sel_trimester').append('<option value="'+ result[i].id + '">'+ result[i].name +'</option>')
                }
                $('#sel_trimester').append('</optgroup>');
                $('#sel_trimester').val(result[0].id).trigger('change');
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
                $('#sel_year').val(result[0].id).trigger('change');
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
        var url = '/document/' + e[0].id + '/';
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

    function move_modal(e){
        console.log('move_moal');
        var url = '/document/ajax/move/' + e[0]['dataset'].id + '/';
        console.log(url);
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                $("#modal_company").empty();
                for (var i=0; i < result['companies'].length;i++){
                    var option = '<option value="' + result['companies'][i].id + '"';
                    option += '>(' + result['companies'][i].id + ') ' + result['companies'][i].name + '</option>';
                    $("#modal_company").append(option);
                }
                $("#modal_company").val(result['company'].id).trigger('change');
                /*$("#modal_year").empty();
                for (var i=0; i < result['years'].length;i++){
                    var option = '<option value="' + result['years'][i].id + '"';
                    option += '>' + result['years'][i].name + '</option>';
                    $("#modal_year").append(option);
                }*/
                $("#modal_year").val(result['year'].id).trigger('change');
                /*
                 $("#modal_trimester").empty();
                for (var i=0; i < result['trimesters'].length;i++){
                    var option = '<option value="' + result['trimesters'][i].id + '"';
                    option += '>(' + result['trimesters'][i].id + ')' + result['trimesters'][i].name + '</option>';
                    $("#modal_trimester").append(option);
                }*/
                $("#modal_trimester").val(result['trimester'].id).trigger('change');
                console.log(result['trimester'].id);
                /*
                 $("#modal_category").empty();
                for (var i=0; i < result['categories'].length;i++){
                    var option = '<option value="' + result['categories'][i].id + '"';
                    option += '>('+ result['categories'][i].id +')' + result['categories'][i].name + '</option>';
                    $("#modal_category").append(option);
                }*/
                $("#modal_category").val(result['category'].id).trigger('change');
            }
        });
    }


    function modal_trimesters(){
        var y = $('#modal_trimester').val();
        var url = '/trimester/' + y + '/list/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                $('#modal_category').empty();
                for( var i = 0; i < result['nav_list'].length; i++ ) {
                    $('#modal_category').append('<option value="'+ result['nav_list'][i].id + '">(' + result['nav_list'][i].id + ') '+ result['nav_list'][i].name +'</option>')
                }
                $('#modal_category').val(result['nav_list'][0].id).trigger('change');
            }
        });
    }

    function modal_years(){
        var y = $('#modal_year').val();
        var url = '/year/' + y + '/list/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                $('#modal_trimester').empty();
                for( var i = 0; i < result.length; i++ ) {
                    $('#modal_trimester').append('<option value="'+ result[i].id + '">('+ result[i].id +')'+ result[i].name +'</option>')
                }
                $('#modal_trimester').val(result[0].id).trigger('change');
                modal_trimesters();
            }
        });
    }

    function modal_companies(){
        var c = $('#modal_company').val();
        var url = '/company/' + c + '/list/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                $('#modal_year').empty();
                for( var i = 0, len = result.length; i < len; i++ ) {
                    $('#modal_year').append('<option value="'+ result[i].id + '">('+ result[i].id + ')'+ result[i].name +'</option>')
                }
                $('#modal_year').append('</optgroup>');
                $('#modal_year').val(result[0].id).trigger('change');
                modal_years();
            }
        });
    }

    $('#modal_company').on('change', function () { modal_companies();});
    $('#modal_year').on('change', function () { modal_years();});
    $('#modal_trimester').on('change', function () { modal_trimesters();});

    function split_modal(e){
        var url = '/document/ajax/split/' + e[0]['dataset'].id + '/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                //$("#modal-title").text(result['name']);
                //$("#modal-body").html(result['img']);
            }
        });
    }

    function merge_modal(e){
        var url = '/document/ajax/merge/' + e[0]['dataset'].id + '/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                //$("#modal-title").text(result['name']);
                //$("#modal-body").html(result['img']);
            }
        });
    }


    function update_datatable(data){
        var out = '<td>';
        var lock = '<td>';
        if (data['lock']){
            lock += '<a class="btn btn-xs btn-default"><span class="glyphicon glyphicon-lock"></span></a>';
        }
        lock += '</td>';
        if (data['complete']){

            out += '<a class="btn btn-xs btn-default split_modal" data-id="'+ data['id'] +'" title="Split" data-toggle="modal" data-target="#myModal"><span class="glyphicon glyphicon-resize-full"></span></a>';
            out += '<a class="btn btn-xs btn-default merge_modal" data-id="'+ data['id'] +'" title="Merge" data-toggle="modal" data-target="#myModal"><span class="glyphicon glyphicon-resize-small"></span></a>';
            out += '<a class="btn btn-xs btn-default move_modal" data-id="'+ data['id'] +'" title="Move" data-toggle="modal" data-target="#modal_move"><span class="glyphicon glyphicon-transfer"></span></a>';
        }
        else{
            out += '<a class="btn btn-xs btn-default"><span class="glyphicon glyphicon-refresh"></span> </a>';
        }
        out += '</td>';
        $('#datatable').dataTable().fnAddData([data['fiscal_id'], "<a id='" + data['id'] + "' class='img_modal' data-toggle='modal' data-target='#myModal'>" + data['name'] + "</a>", data['date'], data['description'], lock, out]);
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
                update_data();
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
        var url = '/trimester/' + t + '/list/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                for (var i = 0; i < result['nav_list'].length; i++) {
                    $("ul.nav-pills li:eq(" + i + ") a").html(result['nav_list'][i]['name'] + ' <span class="badge">'+ result['nav_list'][i]['n'] +'</span>');
                    $("ul.nav-pills li:eq(" + i + ") a").attr( "data-id", result['nav_list'][i]['id']);
                    $("ul.nav.nav-pills li:eq(" + i + ")").removeClass("active");
                }
                $("ul.nav.nav-pills li:eq(0)").addClass("active");
                $('#datatable').dataTable().fnClearTable();
                for (var i = 0; i < result['doc_list'].length; i++) {
                    update_datatable(result['doc_list'][i]);
                }
                $('#pagination').bootpag({total: result['nav_list'][0]['n'], page: 1});
                $('#title_trimester').html(result['title_trimester']);
                view_form(result['valid'], result['img'],result['form'], result['doc_id']);
            }
        });
    }


    function get_form_data(i){
        var cat_id = $('ul.nav-pills li.active a').attr("data-id");
        var url = '/category/' + cat_id + '/form/' + i + '/'; /* TODO a corriger */
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
        var data_id = $('ul.nav-pills li.active a').attr("data-id");
        var id = $('ul.nav-pills li.active a').attr("id");
        var url = '/category/' + data_id + '/add_documents/';
        $.ajax({
            url: url,
            type: 'GET',
            data: {'files':files},
            traditional: true,
            dataType: 'html',
            success: function(result){
                result = JSON.parse(result);
                $('#datatable').dataTable().fnClearTable();
                for (var i = 0; i < result['doc_list'].length; i++) {
                    update_datatable(result['doc_list'][i]);
                    $(".img_modal").click(function(){
                        img_modal($(this));
                    });
                }
                $('ul.nav-pills li.active span').html(result['n']);
            }
        });
    });

    $('ul.nav-pills li a').click(function () {
        $('ul.nav-pills li.active').removeClass('active');
        $(this).parent('li').addClass('active');
        var cat_id = $('ul.nav-pills li.active a').attr("data-id");
        var url = '/category/' + cat_id + '/list/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                $('#datatable').dataTable().fnClearTable();
                for (var i = 0; i < result['doc_list'].length; i++) {
                    update_datatable(result['doc_list'][i]);
                }
                var n = parseInt(result['n']);
                $('#pagination').bootpag({total: n,page: 1}).on("page", function(event, num){
                    get_form_data(num);
                });
                get_form_data(1);
                /* TODO remplacer 1 et nmum */
                $(".img_modal").click(function(){
                    img_modal($(this));
                });
                $(".move_modal").click(function(){
                    move_modal($(this));
                });

                $(".merge_modal").click(function(){
                    merge_modal($(this));
                });

                $(".split_modal").click(function(){
                    split_modal($(this));
                });
            }
        });
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
