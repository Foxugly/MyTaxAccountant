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
                        <li role="presentation" class="active"><a id="{{c.id}}" href="#">{{c.cat.name}} <span class="badge">{{c|len_docs}}</span></a></li>
                    {% else %}
                        <li role="presentation"><a id="b_{{c.id}}" href="#">{{c.cat.name}} <span class="badge">{{c|len_docs}}</span></a></li>
                    {% endif %}
                {% else %}
                    {%if forloop.first %}
                        <li role="presentation" class="active"><a id="{{c.id}}" href="#">{{c.cat.name}} <span class="badge">{{c|len_docs}}</span></a></li>
                    {% else %}
                        <li role="presentation"><a id="{{c.id}}" href="#">{{c.cat.name}} <span class="badge">{{c|len_docs}}</span></a></li>
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
        <table id="example" class="table table-striped table-bordered" width="100%" cellspacing="0">
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
                <tr>
                    <td>1</td>
                    <td>mafacture.pdf</td>
                    <td>05/10/2015</td>
                    <td>electricité</td>
                    <td>validate</td>
                </tr>
                <tr>
                    <td>2</td>
                    <td>facture_restaurant.pdf</td>
                    <td>06/10/2015</td>
                    <td>restaurant</td>
                    <td>treat</td>
                </tr>
            </tbody>
        </table>
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
/*jslint unparam: true */
/*global window, $ */
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$(function () {
    'use strict';
    // Change this to the location of your server-side upload handler:
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
                $("#files-group").append('<li class="list-group-item list-group-item-success">' + file.name + '</li>');
                  
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
    $('#example').DataTable();
} );

$('#valid_files').click(function() {
    var files = []
    $('#files-group').find('li').each(function(){
        var current = $(this);
        console.log(current.text());
        files.push(current.text());
    });
    $('#files-group').empty()
    $("#listfile_row" ).addClass( "hide" );
    var jsonText = JSON.stringify(files);
    var id = $('ul.nav-pills li.active a').attr("id")
    var url = '/category/' + id + '/add_files/';
    console.log(url);
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
$('ul.nav-pills li a').click(function (e) {
  $('ul.nav-pills li.active').removeClass('active')
  $(this).parent('li').addClass('active')

  var id = $('ul.nav-pills li.active a').attr("id")
  var url = '/category/' + id + '/';
  console.log(url);
  /*$.ajax({
        url: url,
        type: 'POST',
        data: jsonText,
        traditional: true,
        dataType: 'html',
        success: function(result){
            location.reload();
        }
    });*/
});
</script>
{% endblock %}
