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
                console.log('beforeSend');
                if (!csrfSafeMethod(settings.type)) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            dataType: 'json',
            done: function (e, data) {
                console.log('done');
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


    $('.select2100').select2({ width: '100%' });
    $('.select2-nosearch').select2({ width: 'resolve', minimumResultsForSearch: -1});
    $('.select2100-nosearch').select2({ width: '100%', minimumResultsForSearch: -1});
    $("#dlb_documents").DualListBox();

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

    $('#sel_trimester').change(function() {update_categories();});
    $('#sel_year').change(function() {update_trimesters();});
    $('#sel_company').change(function() {update_years();});
    $('ul.nav-pills li a').click(function() {nav_click($(this));});
    $('#modal_company').on('change', function () { modal_companies();});
    $('#modal_year').on('change', function () { modal_years();});
    $('#modal_trimester').on('change', function () { modal_trimesters();});

    function update_categories(){
        /*console.log('update_categories');*/
        var url = '/trimester/' + $('#sel_trimester').val() + '/list/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                for (var i = 0; i < result['nav_list'].length; i++) {
                    $("ul.nav-pills li:eq(" + i + ") a").html(result['nav_list'][i]['name'] + ' <span class="badge">'+ result['nav_list'][i]['n'] +'</span>');
                    $("ul.nav-pills li:eq(" + i + ") a").attr( "data-id", result['nav_list'][i]['id']);
                }
                var size = $("ul.nav-pills")[0].childElementCount;
                if (result['nav_list'].length == 1){
                    for (var i = 1 ; i < size; i++){
                        $("ul.nav-pills li:eq(" + i + ")").hide();
                    }
                    $("ul.nav-pills")[0].click();
                }
                else{
                    for (var i = 1 ; i < size; i++){
                        $("ul.nav-pills li:eq(" + i + ")").show();
                    }
                }
                nav_click($('ul.nav-pills li.active a'));
            }
        });
    }

    function update_trimesters(){
        var url = '/year/' + $('#sel_year').val() + '/list/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                $('#sel_trimester').empty().append('<optgroup label = "Choose a trimester">');
                for( var i = 0; i < result['list'].length; i++ ) {
                    $('#sel_trimester').append('<option value="'+ result['list'][i].id + '">'+ result['list'][i].name +'</option>');
                }
                $('#sel_trimester').append('</optgroup>');
                $('#sel_trimester').val(result['favorite'].id).trigger('change');
                update_data(true);
            }
        });
    }

    function update_years(){
        var url = '/company/' + $('#sel_company').val() + '/list/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                $('#sel_year').empty().append('<optgroup label = "Choose a tax year">');
                for( var i = 0, len = result['list'].length; i < len; i++ ) {
                    $('#sel_year').append('<option value="'+ result['list'][i].id + '">'+ result['list'][i].name +'</option>');
                }
                $('#sel_year').append('</optgroup>');
                $('#sel_year').val(result['favorite'].id).trigger('change');
                update_trimesters();
            }
        });
    }

    function close_uploadfile(e){
        var url = '/upload/remove/' + e.attr('id') + '/';
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
        /*console.log('move_modal');*/
        var url = '/document/ajax/move/' + e[0]['dataset'].id + '/';
        /*console.log(url);*/
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                $("#modal_company").empty();
                for (var i=0; i < result['companies'].length;i++){
                    var option = '<option value="' + result['companies'][i].id + '"';
                    option += '>' + result['companies'][i].name + '</option>';
                    $("#modal_company").append(option);
                }
                $("#move_doc_id").val(result['doc_id']);
                $("#modal_company").val(result['company'].id).trigger('change');
                setTimeout(function(){
                    $("#modal_year").val(result['year'].id).trigger('change');
                }, 100);
                setTimeout(function(){
                    $("#modal_trimester").val(result['trimester'].id).trigger('change');
                }, 300);
                setTimeout(function(){
                    $("#modal_category").val(result['category'].id).trigger('change');
                }, 500);
            }
        });
    }

    $('#document_move').click(function document_move(){
        var url = '/document/ajax/move/' + $("#move_doc_id").val() + '/' + $("#modal_category").val() + '/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function () {
                update_categories();
                $('#modal_move').hide();
            }
        });
    });

    function modal_trimesters(){
        /*console.log('modal_trimesters');*/
        var url = '/trimester/' + $('#modal_trimester').val() + '/list/';
        /*console.log(url);*/
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                /*console.log(result);*/
                $('#modal_category').empty();
                for( var i = 0; i < result['nav_list'].length; i++ ) {
                    $('#modal_category').append('<option value="'+ result['nav_list'][i].id + '">'+ result['nav_list'][i].name +'</option>');
                }
                $('#modal_category').select2({ width: 'resolve', minimumResultsForSearch: -1});
                $('#modal_category').val(result['nav_list'][0].id).trigger('change');
            }
        });
    }

    function modal_years(){
        /*console.log('modal_years');*/
        var url = '/year/' + $('#modal_year').val() + '/list/';
        /*console.log(url);*/
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                $('#modal_trimester').empty();
                for( var i = 0; i < result['list'].length; i++ ) {
                    $('#modal_trimester').append('<option value="' + result['list'][i].id + '">' + result['list'][i].name + '</option>');
                }
                $('#modal_trimester').select2({ width: 'resolve', minimumResultsForSearch: -1});
                $('#modal_trimester').val(result['favorite'].id).trigger('change');
            }
        });
    }

    function modal_companies(){
        /*console.log('modal_companies');*/
        var url = '/company/' + $('#modal_company').val() + '/list/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                /*console.log(result);*/
                $('#modal_year').empty();
                for( var i = 0, len = result['list'].length; i < len; i++ ) {
                    $('#modal_year').append('<option value="'+ result['list'][i].id + '">'+ result['list'][i].name +'</option>');
                }
                $('#modal_year').select2({ width: 'resolve', minimumResultsForSearch: -1});
                $('#modal_year').val(result['favorite'].id).trigger('change');
            }
        });
    }

    function split_modal(e){
        var url = '/document/ajax/split/' + e[0]['dataset'].id + '/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                if (result['valid']) {
                    for( var i = 1; i < result['size']; i++ ) {
                        $('#modal_split_cut').append('<option value="' + i + '">' + 'Page ' + i + ' and ' + (i+1) + '</option>');
                    }
                    $('#modal_pagination').bootpag({total: result['size'], page: 1, maxVisible: 10}).on("page", function(event, num){
                        modal_update_img(result['doc_id'], num);
                    });

                    $('#modal_view').html(result['img']);
                    $('#modal_split_doc_id').val(result['doc_id']);
                    $('#modal_split_name').val(result['name']);
                    $('#modal_split_new_name').val(result['nname']);
                    $('#modal_split_cut').val(1).trigger('change');
                    $("#modal_split").show();
                }
                else {
                    bootbox.alert("the document cantains only one page");
                }
            }
        });
    }

    function modal_update_img(doc_id, num){
        var url = '/document/ajax/img/' + doc_id + '/' + num + '/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
               $('#modal_view').html(result['img']);
            }
        });
    }

    function merge_modal(e){
        /*console.log("merge_modal");*/
        var url = '/document/ajax/merge/' + e[0]['dataset'].id + '/';
        $('#modal_merge_doc_id').val(e[0]['dataset'].id);
        $.ajax({
            url: url,
            dataType: "text",
            success: function(data) {
                var ss = $('#dual-list-box-documents').find('select');
                $('option', ss[0]).remove();
                $('option', ss[1]).remove();
                var json = $.parseJSON(data);
                for (var i=0;i<json.length;++i) {
                    $(ss[0]).append($('<option>', {value:json[i].id, text:json[i].name}));
                }
                $("#modal_merge").show();
                $('#dual-list-box-documents').find('div')[1].children[3].click();
            }
        });
    }

    function download(e){
        var url = '/document/ajax/download/' + e[0]['dataset'].id + '/';
        $.ajax({
            url: url,
            dataType: "json",
             success: function(result){
                 if (result["valid"]) {
                     window.open(result['url'], '_blank');
                 }
            }
        });
    }


    function del_modal(e){
        var url = '/document/ajax/delete/' +e.currentTarget['dataset'].id + '/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(){}
        });
    }

    function update_datatable(data){
        /*console.log('update_datatable');*/
        var out = '<td>';
        var lock = '<td>';
        if (data['lock']){
            lock += '<span class="glyphicon glyphicon-lock"></span>';
        }
        lock += '</td>';
        if (data['complete']){
            out += '<a id="btn_sp_'+ data['id']+'" class="btn btn-xs btn-default split_modal" data-id="'+ data['id'] +'" title="Split" data-toggle="modal" data-target="#modal_split"><span class="glyphicon glyphicon-resize-full"></span></a>';
            out += '<a id="btn_me_'+ data['id']+'" class="btn btn-xs btn-default merge_modal" data-id="'+ data['id'] +'" title="Merge" data-toggle="modal" data-target="#modal_merge"><span class="glyphicon glyphicon-resize-small"></span></a>';
            out += '<a id="btn_mv_'+ data['id']+'" class="btn btn-xs btn-default move_modal" data-id="'+ data['id'] +'" title="Move" data-toggle="modal" data-target="#modal_move"><span class="glyphicon glyphicon-transfer"></span></a>';
            out += '<a id="btn_dl_'+ data['id']+'" class="btn btn-xs btn-default" data-id="'+ data['id'] +'" title="Download"><span class="glyphicon glyphicon-download-alt"></span></a>';
            out += '<a id="btn_de_'+ data['id']+'" class="btn btn-xs btn-default del_modal" data-id="'+ data['id'] +'" title="Delete"><span class="glyphicon glyphicon-remove"></span></a>';
        }
        else{
            out += '<a class="btn btn-xs btn-default"><span class="glyphicon glyphicon-refresh"></span> </a>';
        }
        out += '</td>';
        $('#datatable').dataTable().fnAddData([data['fiscal_id'], "<a id='" + data['id'] + "' class='img_modal' data-id='"+ data['id'] +"' data-toggle='modal' data-target='#myModal'>" + data['name'] + "</a>", data['date'], data['description'], lock, out]);
        $("#"+data['id']).click(function(){img_modal($(this));});
        $("#btn_mv_"+data['id']).click(function(){move_modal($(this));});
        $("#btn_me_"+data['id']).click(function(){merge_modal($(this));});
        $("#btn_sp_"+data['id']).click(function(){split_modal($(this));});
        $("#btn_dl_"+data['id']).click(function(){download($(this));});
        $("#btn_de_"+data['id']).click(function(e){
            var btn = $('ul.nav-pills li.active a')[0];
            bootbox.confirm("Are you sure?", function(result) {
                if(result) {
                    del_modal(e);
                    update_data(false);
                    bootbox.alert("Document deleted !", function() {btn.click();});
                }
            });
        });
    }

    function save_form(){
        /*console.log('save_form');*/
        $('#alert_save_error').hide();
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
                if (result['return']){
                    bootbox.alert("Saved!", function(){});
                    $('#alert_save_saved').show().delay( 1000 ).fadeOut(1000);
                }
                else{;
                    var out = '';
                    for (var key in result['errors']){
                        out += result['errors'][key][0] + '<br>';
                    }
                    $('#alert_save_error').html(out);
                    $('#alert_save_error').show();
                }
                update_data(false);
            }
        });
    }

    function view_form(valid, img, form,doc_id){
        /*console.log('view_form');*/
        if (valid == true){
            $('#div_img').html(img);
            $('#div_form').html('<input id="doc_id" type="hidden" name="doc_id" value="' + doc_id + '">' +form);
            $('#id_owner').select2({ width: 'resolve', minimumResultsForSearch: -1});
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

    function update_data(option){
        console.log('update_data');
        var pagnum = $('#pagination').bootpag().find('.active').data()['lp'];
        var url = '/category/'+ $('ul.nav-pills li.active a').attr("data-id") + '/list/' +  pagnum + '/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                $('#datatable').dataTable().fnClearTable();
                var numpage = 1;
                for (var i = 0; i < result['doc_list'].length; i++) {
                    update_datatable(result['doc_list'][i]);
                    if ($('#doc_id').val() == result['doc_list'][i]['id']){
                        numpage = i + 1 ;
                    }
                }
                if (option){
                        $('#pagination').bootpag({total: result['n'], page: numpage, maxVisible: 10,});
                    if (result['doc'] == null){
                        view_form(result['valid'], null, null, 0);
                    }
                    else{
                        view_form(result['valid'], result['doc']['img'],result['form'], $('#doc_id').val());
                    }
                    $('ul.nav-pills li.active a').click();
                }
            }
        });
    }

    function get_form_data(i){
        console.log('get_form_data ');
        var url = '/category/' + $('ul.nav-pills li.active a').attr("data-id") + '/form/' + i + '/';
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
        var files = [];
        $('#files-group').find('li').each(function(){
            var current = $(this).find('span');
            files.push(current.text());
        });
        $('#files-group').empty();
        $("#fileupload_list" ).addClass( "hide" );
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

    function nav_click(e){
        $('ul.nav-pills li.active').removeClass('active');
        e.parent('li').addClass('active');
        var cat_id = $('ul.nav-pills li.active a').attr("data-id");
        var url = '/category/' + cat_id + '/list/1/';
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
                $('#pagination').bootpag({total: n, page: 1, maxVisible: 10}).on("page", function(event, num){
                    console.log('nav_click');
                    var table = $('#datatable').dataTable();
                    console.log(table);
                    var a = table.children().children()[1 + num].children[1];
                    var id = $(a).find("a")[0].id;
                    get_form_data(id);

                });
            }
        });
    }

    $("#view_group :input:radio").change(function() {
        var view = this.value;
        if (view == 'list'){
            $("#div_list").show();
            $("#div_img_form").hide();
            $('#alert_save_saved').hide();
            $('#alert_save_error').hide();
        }
        else if (view == 'form'){
            $("#div_list").hide();
            $("#div_img_form").show();
            $('#alert_save_saved').hide();
            $('#alert_save_error').hide();
            get_form_data($('#pagination').bootpag().find('.active').data()['lp']);
        }
    });

    $('#pagination').bootpag({
            total: 1,
            page: 1,
            maxVisible: 10,
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

    $('#document_split').click(function() {
        var form = $('#form_split');
        var url = '/document/split/';
        $.ajax({
            url: url,
            type: 'GET',
            data: form.serialize(),
            traditional: true,
            dataType: 'json',
            success: function(){
                update_categories();
            }
        });
    });

    $('#document_merge').click(function() {
        var data = $('#form_merge').serializeArray();
        var l = [];
        var select = $('#dual-list-box-documents').find('select')[1];
        for (var i = 0 ; i < select.length ; i++){
            l.push(select[i].value);
        }
        data.push({name: 'doc_ids', value: l});
        var url = '/document/merge/';
        $.ajax({
            url: url,
            type: 'GET',
            data: data,
            traditional: true,
            dataType: 'json',
            success: function(){
                update_categories();
            }
        });
    });
});
