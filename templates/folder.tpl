{% extends "layout.tpl" %}
{% load staticfiles %}
{% load favorite %}
{% load upload_tags %}
{% load details_cat %}
{% load tools %}
{% block header %}
<link rel="stylesheet" href="https://cdn.datatables.net/1.10.9/css/dataTables.bootstrap.min.css">
<link rel="stylesheet" href=" {% static "upload/css/style.css" %} ">
<link rel="stylesheet" href=" {% static "upload/css/jquery.fileupload-ui.css" %}" >
{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-8 col-md-offset-2">
        <ul class="nav nav-tabs nav-pills" role="tablist">
            {% for c in userprofile|companies|years|trimesters|categories %}
                {% if category %}
                    {%if c == category %}
                        <li role="presentation" class="active"><a data-target="#" data-toggle="pill" id="{{c.id}}" href="#">{{c.cat.name}} <span class="badge">{{c|len_docs}}</span></a></li>
                    {% else %}
                        <li role="presentation"><a data-target="#" data-toggle="pill" id="b_{{c.id}}" href="#">{{c.cat.name}} <span class="badge">{{c|len_docs}}</span></a></li>
                    {% endif %}
                {% else %}
                    {%if forloop.first %}
                        <li role="presentation" class="active"><a data-target="#" data-toggle="pill" id="{{c.id}}" href="#">{{c.cat.name}} <span class="badge">{{c|len_docs}}</span></a></li>
                    {% else %}
                        <li role="presentation"><a data-target="#" data-toggle="pill" id="{{c.id}}" href="#">{{c.cat.name}} <span class="badge">{{c|len_docs}}</span></a></li>
                    {% endif %}
                {% endif %}
            {% endfor %}
        </ul>
    </div>
</div>
<div class="row" style="margin-top:20px;margin-bottom:20px;">
    <div class="col-md-6 col-md-offset-2">
       <span class="btn btn-success fileinput-button">
            <i class="glyphicon glyphicon-plus"></i>
            <span>Upload files</span>
            <input id="fileupload" type="file" name="file" multiple>
        </span>
    </div>
    <div class="col-md-2 text-right">
        <div class="btn-group " role="group" aria-label="...">
            <button type="button" class="btn btn-default active"><span class="glyphicon glyphicon-list"></span></button>
            <button type="button" class="btn btn-default"><span class="glyphicon glyphicon-file"></span></button>
        </div>
    </div>
</div>
<div id="progress_row" class="row hide">
    <div id="progress" class="progress col-md-6 col-md-offset-2">
            <div class="progress-bar progress-bar-success"></div>
    </div>
</div>
<div id="listfile_row" class="row hide">
    <div class="col-md-5 col-md-offset-2">
        <ul id="files-group" class="list-group"></ul>
    </div>
    <div class="col-md-1">
        <a id="valid_files" href="#" class="btn btn-primary btn-primary"><span class="glyphicon glyphicon-ok"></span> Validate</a>
    </div>
</div>
<div class="row">
    <div class="col-md-8 col-md-offset-2">
        <table id="datatable" class="table table-striped table-bordered" width="100%" cellspacing="0">
            <thead>
                <tr>
                    <th>NumberID</th>
                    <th>Name</th>
                    <th>Date</th>
                    <th>Comments</th>
                    <th>Status</th>
                </tr>
            </thead>
     
            <tfoot>
                <tr>
                    <th>NumberID</th>
                    <th>Name</th>
                    <th>Date</th>
                    <th>Comments</th>
                    <th>Status</th>
                </tr>
            </tfoot>
     
            <tbody>
                {% if category %}
                    {% for c in userprofile|companies|years|trimesters|categories %}
                        {% if c == category %}
                            {% for d in c|documents %}
                                <tr><td>{{d.id}}</td><td><a id={{d.id}} class='img_modal' data-toggle="modal" data-target="#myModal">{{d.name}}</a></td><td>{{d.date}}</td><td>{{d.description}}</td><td>{{d.complete}}</td></tr>
                            {% endfor %}
                        {% endif %}
                    {% endfor %}
                {% else %}
                    {% for c in userprofile|companies|years|trimesters|categories %}
                        {% if forloop.first %}
                            {% for d in c.documents.all %}
                                <tr><td>{{d.id}}</td><td><a id={{d.id}} class='img_modal' data-toggle="modal" data-target="#myModal">{{d.name}}</a></td><td>{{d.date}}</td><td>{{d.description}}</td><td>{{d.complete}}</td></tr>
                            {% endfor %}
                        {% endif %}
                    {% endfor %}
                {% endif %}
            </tbody>
        </table>
    </div>
</div>
<!-- Modal -->
<div class="modal fade" id="myModal" role="dialog">
    <div class="modal-dialog modal-lg">
        <!-- Modal content-->
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">&times;</button>
                <h4 id='modal-title' class="modal-title"></h4>
            </div>
            <div id='modal-body' class="modal-body"></div>
            <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block js %} 
<script type="text/javascript" src="http://cdn.datatables.net/1.10.9/js/jquery.dataTables.js"></script>
<script type="text/javascript" src="http://cdn.datatables.net/1.10.9/js/dataTables.bootstrap.min.js"></script>
<script src=" {% static "upload/js/vendor/jquery.ui.widget.js" %}"></script>
<script src=" {% static "upload/js/jquery.iframe-transport.js" %}"></script>
<script src=" {% static "upload/js/jquery.fileupload.js" %}"></script>
<script src=" {% static "upload/js/jquery.cookie.js" %}"></script>
<script>
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
            $.each(data.result.files, function (index, file) {
                $("#listfile_row" ).removeClass( "hide" );
                $("#files-group").append('\n<li class="list-group-item list-group-item-success">' + file.name + '</li>\n'); 
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

$(document).ready(function() {
    $('#datatable').DataTable();
    console.log('READY');
} );

$('#valid_files').click(function() {
    var files = []
    $('#files-group').find('li').each(function(){
        var current = $(this);
        files.push(current.text());
    });
    $('#files-group').empty()
    $("#listfile_row" ).addClass( "hide" );
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
            console.log('back from ajax');
        }
    });
});

function img_modal(){
    var id = $(this).attr('id');
    console.log(id);
    var url = '/document/' + id + '/';
    console.log(url);
    $.ajax({
        url: url,
        type: 'GET',
        traditional: true,
        dataType: 'json',
        success: function(result){
            console.log('retour');
            $("#modal-title").text(result['name']);
            $("#modal-body").html(result['img']);
        }
    });
}

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
            $('#datatable tbody').empty();
            for (i = 0; i < result['data'].length; i++) {
                $('#datatable tbody').append('<tr><td>'+result['data'][i]['id']+"</td><td><a id='" + result['data'][i]['id'] + "' class='img_modal' data-toggle='modal' data-target='#myModal'>" + result['data'][i]['name'] + '</a></td><td>'+result['data'][i]['date']+'</td><td>'+result['data'][i]['description']+'</td><td>' + result['data'][i]['complete']+ '</td></tr>');
                $(".img_modal").click(function(){
                    img_modal();
                });
            }
            $('#datatable').DataTable();
        }
    });
});

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

            }
            $("ul.nav.nav-pills li:eq(0)").addClass("active");
            $('#datatable tbody').empty();
            for (i = 0; i < result['doc_list'].length; i++) {
                $('#datatable tbody').append("<tr><td>" + result['doc_list'][i]['id'] + "</td><td><a id='" + result['doc_list'][i]['id'] + "' class='img_modal' data-toggle='modal' data-target='#myModal'>" + result['doc_list'][i]['name'] + "</a></td><td>" + result['doc_list'][i]['date'] + "</td><td>" + result['doc_list'][i]['description'] + "</td><td>" + result['doc_list'][i]['complete'] + "</td></tr>");
                $(".img_modal").click(function(){
                    img_modal();
                });
            }
            $('#datatable').DataTable();

        }
    });
}


$(".img_modal").click(function(){
    img_modal();
});
</script>
{% endblock %}
