/**
 * Created by renaud on 03/02/16.
 */

var DEBUG = true;

/**
 *  fileupload
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
    $('.select2100').select2({ width: '100%' });
    $('.select2-nosearch').select2({ width: 'resolve', minimumResultsForSearch: -1});
    $('.select2100-nosearch').select2({ width: '100%', minimumResultsForSearch: -1});
    $("#dlb_documents").DualListBox();
    $('#btn_save').click(function(){save_form();});
    $('#btn_save_next').click(function(){save_next_form();});
    $('#confirm_yes_close').click(function(){$('#confirm_yes').hide();});
    $('#confirm_yes_ok').click(function(){$('#confirm_yes').hide();});
    $('#confirm_no_close').click(function(){$('#confirm_no').hide();});
    $('#confirm_no_ok').click(function(){$('#confirm_no').hide();});

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

    $('#sel_trimester').change(function() {window.location ='/trimester/' + $('#sel_trimester').val() + '/'});
    $('#sel_year').change(function() {update_trimesters();});
    $('#sel_company').change(function() {update_years();});
    //$('#nav_category li a').click(function() {nav_click($(this));});
    $('#modal_company').on('change', function () { modal_companies();});
    $('#modal_year').on('change', function () { modal_years();});
    $('#modal_trimester').on('change', function () { modal_trimesters();});
    $(".img_modal").click(function(){img_modal($(this));});
    $(".move_modal").click(function(){move_modal($(this));});
    $(".merge_modal").click(function(){merge_modal($(this));});
    $(".split_modal").click(function(){split_modal($(this));});
    $(".download").click(function(){download($(this));});
    $(".view").click(function(){view($(this));});
    $(".fiche").click(function(){fiche($(this));});
    $(".del_modal").click(function(){
        var obj = $(this);
        var btn = $('ul.nav-pills li.active a')[0];
        bootbox.confirm({
            message: "Are you sure ?",
            buttons : {
                confirm: {
                    label: 'Yes',
                    className: 'btn-success'
                },
                cancel: {
                    label: 'No',
                    className: 'btn-danger'
                }
            },
            callback: function (result) {
                if (result) {
                    del_modal(obj);
                }
            }
        });
    });

    function update_categories(){
        var url = '/trimester/' + $('#sel_trimester').val() + '/forward/';
        if (DEBUG) {
            console.log('update_categories');
            console.log(url);
        }
        var url = '/trimester/' + $('#sel_trimester').val() + '/forward/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                if (result['forward']) {
                    console.log(result['forward']);
                    window.location.replace(result['forward']);
                }
            },
            error: function(){
                bootbox.alert("[update_categories] ERROR with " + url);
                return 0;
            },
        });
    }

    function update_trimesters(){
        var url = '/year/' + $('#sel_year').val() + '/forward/';
        if (DEBUG) {
            console.log('update_trimesters');
            console.log(url);
        }
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                if (result['forward']) {
                    console.log(result['forward']);
                    window.location.replace(result['forward']);
                }
            },
            error: function(){
                bootbox.alert("[update_trimesters] ERROR with " + url);
                return 0;
            },
        });
    }

    function update_years(){
        var url = '/company/' + $('#sel_company').val() + '/forward/';
        if (DEBUG) {
            console.log('update_years');
            console.log(url);
        }
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                if (result['forward']) {
                    console.log(result['forward']);
                    window.location.replace(result['forward']);
                }
            },
            error: function(){
                bootbox.alert("[update_years] ERROR with " + url);
                return 0;
            },
        });
    }

    function close_uploadfile(e){
        var url = '/upload/remove/' + e.attr('id') + '/';
        if (DEBUG) {
            console.log("close_uploadfile");
            console.log(url);
        }
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
        if (DEBUG) {
            console.log("img_modal :" + e);
            console.log(url);
        }
        var url = '/document/' + e[0].id + '/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                $("#modal-title").text(result['name']);
                $("#modal-body").html(result['img']);
            },
            error: function(){
                bootbox.alert("[img_modal] ERROR with " + url);
                return 0;
            },
        });
    }

    function move_modal(e){
        var url = "/document/ajax/move/" + e[0]['dataset'].id + "/";
        if (DEBUG) {
            console.log('move_modal');
            console.log(url);
        }
        $("#document_move").show();
        $("#document_multiple_move").hide();
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
                }, 400);
                setTimeout(function(){
                    $("#modal_category").val(result['category'].id).trigger('change');
                }, 700);
            },
            error: function(){
                bootbox.alert("[move_modal] ERROR with " + url);
                return 0;
            },
        });
    }

    $('#document_move').click(function document_move(){
        var url = "/document/ajax/move/" + $("#move_doc_id").val() + "/" + $("#modal_category").val() + "/";
        if (DEBUG) {
            console.log("#document_move");
            console.log(url);
        }
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function () {
                //update_categories();
                //document_move
                window.location.reload();
            },
            error: function(){
                bootbox.alert("[click on document_move] ERROR with " + url);
                return 0;
            },
        });
    });

    $('#document_split').click(function() {
        var form = $('#form_split');
        var url = '/document/split/';
        if (DEBUG) {
            console.log("#document_split");
            console.log(url);
        }
        $.ajax({
            url: url,
            type: 'GET',
            data: form.serialize(),
            traditional: true,
            dataType: 'json',
            success: function(){
                window.location.reload()
            }
        });
    });

    $('#document_merge').click(function() {
        if (DEBUG) {
            console.log("#document_merge");
        }
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
                //update_categories();
                window.location.reload()
            }
        });
    });

    function modal_trimesters(){
        var url = '/trimester/' + $('#modal_trimester').val() + '/list/';
        if (DEBUG) {
            console.log('modal_trimesters');
            console.log(url);
        }
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                $('#modal_category').empty();
                for( var i = 0; i < result['nav_list'].length; i++ ) {
                    $('#modal_category').append('<option value="'+ result['nav_list'][i].id + '">'+ result['nav_list'][i].name +'</option>');
                }
                $('#modal_category').select2({ width: 'resolve', minimumResultsForSearch: -1});
                $('#modal_category').val(result['nav_list'][0].id).trigger('change');
            },
            error: function(){
                bootbox.alert("[modal_trimesters] ERROR with " + url);
                return 0;
            },
        });
    }

    function modal_years(){
        var url = '/year/' + $('#modal_year').val() + '/list/';
        if (DEBUG) {
            console.log('modal_years');
            console.log(url);
        }
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
            },
            error: function(){
                bootbox.alert("[modal_years] ERROR with " + url);
                return 0;
            },
        });
    }

    function modal_companies(){
        var url = '/company/' + $('#modal_company').val() + '/list/';
        if (DEBUG) {
            console.log('modal_companies');
            console.log(url);
        }
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                $('#modal_year').empty();
                for( var i = 0, len = result['list'].length; i < len; i++ ) {
                    $('#modal_year').append('<option value="'+ result['list'][i].id + '">'+ result['list'][i].name +'</option>');
                }
                $('#modal_year').select2({ width: 'resolve', minimumResultsForSearch: -1});
                $('#modal_year').val(result['favorite'].id).trigger('change');
            },
            error: function(){
                bootbox.alert("[modal_companies] ERROR with " + url);
                return 0;
            },
        });
    }

    function split_modal(e){
        var url = '/document/ajax/split/' + e[0]['dataset'].id + '/';
        if (DEBUG) {
            console.log("split_modal");
            console.log(url);
        }
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
            },
            error: function(){
                bootbox.alert("[split_modal] ERROR with " + url);
                return 0;
            },
        });
    }

    function modal_update_img(doc_id, num){
        var url = '/document/ajax/img/' + doc_id + '/' + num + '/';
        if (DEBUG) {
            console.log("modal_update_img");
            console.log(url);
        }
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
               $('#modal_view').html(result['img']);
            },
            error: function(){
                bootbox.alert("[modal_update_img] ERROR with " + url);
                return 0;
            },
        });
    }

    function merge_modal(e){
        var url = '/document/ajax/merge/' + e[0]['dataset'].id + '/';
        if (DEBUG) {
            console.log("merge_modal");
            console.log(url);
        }
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
            },
            error: function(){
                bootbox.alert("[merge_modal] ERROR with " + url);
                return 0;
            },
        });
    }

    function download(e){
        var url = '/document/ajax/download/' + e[0]['dataset'].id + '/';
        if (DEBUG) {
             console.log("download");
             console.log(url);
        }
        $.ajax({
             url: url,
             dataType: "json",
             success: function(result){
                 if (result["valid"]) {
                      window.open(result['url'], '_blank');
                 }
            },
            error: function(){
                bootbox.alert("[download] ERROR with " + url);
                return 0;
            },
        });
    }

    function view(e){
        var url = '/document/view/' + e[0]['dataset'].id + '/';
        if (DEBUG) {
             console.log("view");
             console.log(url);
        }
         window.open(url, '_blank');
    }

    function fiche(e){
        var pathname = window.location.pathname; // Returns path only
        var parts = pathname.split('/');
        var field = $('#datatable').dataTable().fnSettings().aaSorting[0][0];
        var sens = $('#datatable').dataTable().fnSettings().aaSorting[0][1];
        var n_in_page = e.closest('tr').index() + 1;
        var n_length_page = $('#datatable').DataTable().page.info().length;
        var n_current_page = $('#datatable').DataTable().page.info().page;
        var n = (n_length_page * n_current_page) + n_in_page;
        var url = parts[0] + '/' + parts[1] + '/' + parts[2] + '/form/' + field + '/' + sens + '/' + n + '/';
        console.log(url);
        window.location.replace(url);
    }

    function del_modal(e){
        var url = '/document/ajax/delete/' + e[0]['dataset'].id + '/';
        if (DEBUG) {
            console.log("del_modal");
            console.log(url);
        }
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(){
                window.location.reload();
            },
            error: function(){
                bootbox.alert("[del_modal] ERROR with " + url);
                return 0;
            },
        });
    }

    function update_datatable(data){
        if (DEBUG) {
            console.log('update_datatable');
        }

        var lock = '<td>';
        if (data['lock']){
            lock += '<span class="glyphicon glyphicon-lock"></span>';
        }
        lock += '</td>';
        var repeat = false;
        var out = '<td>';
        if (data['complete']){
            out += '<a id="btn_vi_'+ data['id']+'" class="btn btn-xs btn-default view" data-id="'+ data['id']+'" title="View"><span class="glyphicon glyphicon-eye-open"></span></a>';
            out += '<a id="btn_fi_'+ data['id']+'" class="btn btn-xs btn-default fiche" data-id="'+ data['id']+'" title="Fiche"><span class="glyphicon glyphicon-file"></span></a>';
            out += '<a id="btn_sp_'+ data['id']+'" class="btn btn-xs btn-default split_modal" data-id="'+ data['id'] +'" title="Split" data-toggle="modal" data-target="#modal_split"><span class="glyphicon glyphicon-resize-full"></span></a>';
            out += '<a id="btn_me_'+ data['id']+'" class="btn btn-xs btn-default merge_modal" data-id="'+ data['id'] +'" title="Merge" data-toggle="modal" data-target="#modal_merge"><span class="glyphicon glyphicon-resize-small"></span></a>';
            out += '<a id="btn_mv_'+ data['id']+'" class="btn btn-xs btn-default move_modal" data-id="'+ data['id'] +'" title="Move" data-toggle="modal" data-target="#modal_move"><span class="glyphicon glyphicon-transfer"></span></a>';
            out += '<a id="btn_dl_'+ data['id']+'" class="btn btn-xs btn-default download" data-id="'+ data['id'] +'" title="Download"><span class="glyphicon glyphicon-download-alt"></span></a>';
            out += '<a id="btn_de_'+ data['id']+'" class="btn btn-xs btn-default del_modal" data-id="'+ data['id'] +'" title="Delete"><span class="glyphicon glyphicon-remove"></span></a>';
        }
        else{
            out += '<a class="btn btn-xs btn-default"><span class="glyphicon glyphicon-refresh"></span> </a>';
            repeat = true;
        }
        out += '</td>';
        $('#datatable').dataTable().fnAddData([
            "<input class='select-checkbox type='checkbox' name='select-id[]' value=''>",
            data['fiscal_id'],
            data['id'],
            "<a id='" + data['id'] + "' class='img_modal' data-id='"+ data['id'] +"' data-toggle='modal' data-target='#myModal'>" + data['name'] + "</a>",
            data['date'],
            data['description'],
            lock,
            out
        ]);
        $("#"+data['id']).click(function(){img_modal($(this));});
        $("#btn_vi_"+data['id']).click(function(){view($(this));});
        $("#btn_fi_"+data['id']).click(function(){fiche($(this));});
        $("#btn_mv_"+data['id']).click(function(){move_modal($(this));});
        $("#btn_me_"+data['id']).click(function(){merge_modal($(this));});
        $("#btn_sp_"+data['id']).click(function(){split_modal($(this));});
        $("#btn_dl_"+data['id']).click(function(){download($(this));});
        $("#btn_de_"+data['id']).click(function(){
            var btn = $('ul.nav-pills li.active a')[0];
            bootbox.confirm({
                message: "Are you sure ?",
                buttons : {
                    confirm: {
                        label: 'Yes',
                        className: 'btn-success'
                    },
                    cancel: {
                        label: 'No',
                        className: 'btn-danger'
                    }
                },
                callback: function (result) {
                    if (result) {
                        del_modal($(this));
                    }
                }
            });
        });
        return repeat;
    }

    function save_form() {
        if (DEBUG){
            console.log('save_form');
        }
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
                        out += result['errors'][key][0];
                    }
                    $('#alert_save_error').html(out);
                    $('#alert_save_error').show();
                }
            }
        });
    }

    function save_next_form() {
        if (DEBUG){
            console.log('save_form');
        }
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
                    var url = window.location.href;
                    var split = url.split("/");
                    var next = "";
                    for (var i = 0 ; i < (split.length)-2; i = i +1){
                        next += split[i] + "/";
                    }
                    var next_n = parseInt(split[split.length-2])+1;
                    if (next_n <= result['n']){
                        next += next_n + "/";
                        window.location.href = next;
                    }
                    else{
                        bootbox.alert("Saved!", function(){});
                        $('#alert_save_saved').show().delay( 1000 ).fadeOut(1000);
                    }
                }
                else{;
                    var out = '';
                    for (var key in result['errors']){
                        out += result['errors'][key][0];
                    }
                    $('#alert_save_error').html(out);
                    $('#alert_save_error').show();
                }
            }
        });
    }
    function update_data(option, nb){
        var pagnum = $('#pagination').bootpag().find('.active').data()['lp'];
        var url = '/category/'+ $('ul.nav-pills li.active a').attr("data-id") + '/list/' +  pagnum + '/';
        if (DEBUG) {
            console.log('update_data');
            console.log(url);
        }
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                $('#datatable').dataTable().fnClearTable();
                var numpage = 1;
                var repeat = false;
                for (var i = 0; i < result['doc_list'].length; i++) {
                    var res_return = update_datatable(result['doc_list'][i]) ;
                    repeat = res_return || repeat;
                    if ($('#doc_id').val() == result['doc_list'][i]['id']){
                        numpage = i + 1 ;
                    }
                }
                if (option){
                        $('#pagination').bootpag({total: result['n'], page: numpage, maxVisible: 10,});
                    if (result['doc'] == null){
                        view_form(result['valid'], null, "", 0);
                    }
                    else{
                        view_form(result['valid'], result['doc']['img'],result['form'], $('#doc_id').val());
                    }
                    $('ul.nav-pills li.active a').click();
                }
                if (repeat && nb < 5){
                    setTimeout(function(){ update_data(option, nb+1);}, 4000);
                }
            }
        });

    }

    function get_form_data(i){
        if (DEBUG) {
            console.log('get_form_data ');
            console.log("caller is " + arguments.callee.caller.toString());
        }
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
        var url = '/category/' + data_id + '/add_documents/';
        var repeat = false;
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
                    var res_return = update_datatable(result['doc_list'][i]);
                    repeat = repeat || res_return;
                    $(".img_modal").click(function(){
                        img_modal($(this));
                    });
                }
                $('ul.nav-pills li.active span').html(result['n']);
                if (repeat){
                    setTimeout(function(){ update_data(true,1);}, 4000);
                }
            }
        });
    });

    function nav_click(e){
        if (DEBUG){
            console.log('nav_click');
        }
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
                    var res_return = update_datatable(result['doc_list'][i]);
                }
                view_form(false, null, "", 0);
                var n = parseInt(result['n']);
                    var table = $('#datatable').DataTable().data();
                    if (table.rows().count() > 0){
                        var a = table.rows().data()[0][1];
                        get_form_data($(a).data().id);
                    }else{
                        view_form(false, null, "", 0);
                    }
                $('#pagination').bootpag({total: n, page: 1, maxVisible: 10}).on("page", function(event, num){
                    var table = $('#datatable').DataTable().data();
                    if (table.rows().count() > 0){
                        var a = table.rows().data()[num-1][1];
                        get_form_data($(a).data().id);
                    }else{
                        view_form(false, null, "", 0);
                    }
                });
            }
        });
    }
});
