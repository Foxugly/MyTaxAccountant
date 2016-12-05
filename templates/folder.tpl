{% extends "layout.tpl" %}
{% load staticfiles %}
{% load favorite %}
{% load upload_tags %}
{% load details_cat %}
{% load tools %}
{% load i18n %}
{% block content %}
{% if user.is_authenticated %}
<div class="row">
    <div class="col-md-12">
        <h1 class="text-center" id="title_trimester"><!-- user|favorite_company|favorite_year|favorite_trimester --></h1>
    </div>
</div>
<div class="row">
    <div class="col-md-12">
        <ul id="nav_category" class="nav nav-tabs nav-pills" role="tablist">
            {% for c in user|favorite_company|favorite_year|favorite_trimester|categories %}
                {%if forloop.first %}
                    <li role="presentation" class="active"><a data-target="#" data-id="{{c.id}}" data-toggle="pill" id="nav_{{c.id}}" href="#">{{c.cat.name}} <span class="badge">{{c|len_docs}}</span></a></li>
                {% else %}
                    <li role="presentation"><a data-target="#" data-toggle="pill" data-id="{{c.id}}" id="nav_{{c.id}}" href="#">{{c.cat.name}} <span class="badge">{{c|len_docs}}</span></a></li>
                {% endif %}
            {% endfor %}
        </ul>
    </div>
</div>
<div class="row" style="margin-top:10px;margin-bottom:10px;">
    <div class="col-md-10">
       <span class="btn btn-success fileinput-button">
            <i class="glyphicon glyphicon-plus"></i>
            <span>{% blocktrans %} Upload files {% endblocktrans %} </span>
            <input id="fileupload" type="file" name="file" multiple>
        </span>
    </div>
    <div class="col-md-2 text-right">
        <div id="view_group" class="btn-group" data-toggle="buttons">
            <label class="btn btn-default">
                <input id="input_view_list" name="view_data" value="list" type="radio"><span class="glyphicon glyphicon-list"></span>
            </label>
            <label class="btn btn-default">
                <input id="input_view_form" name="view_data" value="form" type="radio"><span class="glyphicon glyphicon-file"></span>
            </label>
        </div>
    </div>
</div>
<div id="progress_row" class="row hide"><!-- hide -->
    <div id="progress" class="progress col-md-6">
            <div class="progress-bar progress-bar-success"></div>
    </div>
</div>
<div id="fileupload_list" class="row hide"><!-- hide -->
    <div class="col-md-5">
        <ul id="files-group" class="list-group"></ul>
    </div>
    <div class="col-md-1">
        <a id="valid_files" href="#" class="btn btn-primary btn-primary"><span class="glyphicon glyphicon-ok"></span> Validate</a>
    </div>
</div>
<div id="div_list" class="row">
    <div class="col-md-12">
        <table id="datatable" class="table table-striped table-bordered" width="100%" cellspacing="0">
            <thead>
                <tr>
                    <th>{% trans "FiscalID" %}</th>
                    <th>{% trans "Name" %}</th>
                    <th>{% trans "Date" %}</th>
                    <th>{% trans "Comments" %}</th>
                    <th>{% trans "Lock" %}</th>
                    <th>{% trans "Operations" %}</th>
                </tr>
            </thead>
     
            <tfoot>
                <tr>
                    <th>{% trans "FiscalID" %}</th>
                    <th>{% trans "Name" %}</th>
                    <th>{% trans "Date" %}</th>
                    <th>{% trans "Comments" %}</th>
                    <th>{% trans "Lock" %}</th>
                    <th>{% trans "Operations" %}</th>
                </tr>
            </tfoot>
     
            <tbody>
            </tbody>
        </table>
    </div>
</div>
<div id="div_img_form" class="row">
    <div id="div_img" class="col-md-6 docs-gallery" style="width:50%;height: 600px;overflow-y: auto; text-align:center;">
    </div>
    <div class="col-md-6">
        <div id="div_info" width="100%" style="min-height:55px;">
            <div id="alert_save_saved" class="alert alert-success" role="alert">{% blocktrans %} Saved !{% endblocktrans %}</div>
            <div id="alert_save_error" class="alert alert-danger" role="alert"></div>
        </div>
        <div id="div_form" width="100%"></div>
        <div id="div_pager" width="100%" style="text-align:center;">
            <p id="pagination"></p>
        </div>
    </div>
</div>
<!-- Modal -->
<div class="modal fade" id="myModal" role="dialog">
    <div class="modal-dialog modal-lg modal-sm">
        <!-- Modal content-->
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">&times;</button>
                <h4 id='modal-title' class="modal-title"></h4>
            </div>
            <div id='modal-body' class="modal-body" style="text-align:center;"></div>
            <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
            </div>
        </div>
    </div>
</div>
<!-- Modal -->
<div class="modal fade" id="modal_move">
    <div class="modal-dialog">
        <!-- Modal content-->
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">&times;</button>
                <h4 id='modal-title' class="modal-title"></h4>
            </div>
            <div id='modal-body' class="modal-body" style="text-align:center;">
                <form class="form-horizontal">
                    <input type="hidden" id="move_doc_id" value="">
                    <div class="form-group">
                        <label class="col-md-4 col-sm-4 control-label" for="modal_company">{% trans "Company" %}</label>
                        <div class="col-md-8 col-sm-8">
                        <select id="modal_company" name="modal_company" class="form-control  select2-nosearch" style="width: 200px;">
                        </select>
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="col-md-4 col-sm-4 control-label" for="modal_year">{% trans "Year" %}</label>
                        <div class="col-md-8 col-sm-8">
                        <select id="modal_year" name="modal_year" class="form-control  select2-nosearch" style="width: 200px;">
                        </select>
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="col-md-4 col-sm-4 control-label" for="modal_trimester">{% trans "Trimester" %}</label>
                        <div class="col-md-8 col-sm-8">
                        <select id="modal_trimester" name="modal_trimester" class="form-control select2-nosearch" style="width: 200px;">
                        </select>
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="col-md-4 col-sm-4 control-label" for="modal_category">{% trans "Category" %}</label>
                        <div class="col-md-8 col-sm-8">
                        <select id="modal_category" name="modal_category" class="form-control  select2-nosearch" style="width: 200px;">
                        </select>
                        </div>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">{% trans "Close" %}</button>
                <button id="document_move" type="button" class="btn btn-primary" data-dismiss="modal">{% trans "Move" %}</button>
            </div>
        </div>
    </div>
</div>
<!-- Modal -->
<div class="modal fade" id="modal_split">
    <div class="modal-dialog">
        <!-- Modal content-->
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">&times;</button>
                <h4 id='modal_split_title' class="modal-title"></h4>
            </div>
            <div id='modal-body' class="modal-body" style="text-align:center;">
                <div id="modal_view"></div>
                <div id="modal_pager" width="100%" style="text-align:center;">
                    <p id="modal_pagination"></p>
                </div>

                <form id='form_split' class="form-horizontal">
                    <input type="hidden" id="modal_split_doc_id" name="modal_split_doc_id">

                    <div class="form-group">
                        <label class="col-md-4 col-sm-4 control-label" for="modal_split_name">{% trans "Current name" %}</label>
                        <div class="col-md-8 col-sm-8">
                        <input id="modal_split_name" name="modal_split_name" class="form-control">
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="col-md-4 col-sm-4 control-label" for="modal_company">{% trans "Split between" %}</label>
                        <div class="col-md-8 col-sm-8 text-left">
                        <select id="modal_split_cut" name="modal_split_cut" class="form-control  select2-nosearch" style="width: 200px;">
                        </select>
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="col-md-4 col-sm-4 control-label" for="modal_split_new_name">{% trans "Name of the new document" %}</label>
                        <div class="col-md-8 col-sm-8">
                        <input id="modal_split_new_name" name="modal_split_new_name" class="form-control">
                        </div>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">{% trans "Close" %}</button>
                <button id="document_split" type="button" class="btn btn-primary" data-dismiss="modal">{% trans "Split" %}</button>
            </div>
        </div>
    </div>
</div>
<!-- Modal -->
<div class="modal fade" id="modal_merge">
    <div class="modal-dialog  modal-lg">
        <!-- Modal content-->
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">&times;</button>
                <h4 id='modal_split_title' class="modal-title"></h4>
            </div>
            <div id='modal-body' class="modal-body" style="text-align:center;">
                <form id='form_merge' class="form-horizontal">
                    <input type="hidden" id="modal_merge_doc_id" name="modal_merge_doc_id">
                    <div class="row">
                        <div id="dlb_merge" class="col-md-12 col-sm-12 text-center">
                        <select id="dlb_documents" name="dlb_documents" multiple="multiple" data-title="documents" data-source="static/data.json"  data-value="index" data-text="name"></select>
                        </div>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">{% trans "Close" %}</button>
                <button id="document_merge" type="button" class="btn btn-primary" data-dismiss="modal">{% trans "Merge" %}</button>
            </div>
        </div>
    </div>
</div>
{%  endif %}
{% endblock %}

{%  block css %}
    <link rel="stylesheet" href=" {% static "viewer/viewer.min.css" %} ">
{%  endblock %}

{% block js %}
<script>
$(document).ready(function() {
    var datatable = $('#datatable').DataTable( {
            "language": {
                "url": "/static/datatables/i18n/{{ LANGUAGE_CODE }}.lang"
            }
        } );
    $("#div_img_form").hide();
    $('#input_view_list').click();
    $('#sel_company').change();
    $('#pagination').bootpag({total: {{ user|favorite_company|favorite_year|favorite_trimester|categories|first|len_docs }}, page: 1});

});
</script>
<script src=" {% static "viewer/viewer.min.js" %}"></script>
<script src=" {% static "viewer/main.js" %}"></script>
{% endblock %}
