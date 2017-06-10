{% extends "folder.tpl" %}
{% load staticfiles %}
{% load favorite %}
{% load upload_tags %}
{% load details_cat %}
{% load tools %}
{% load i18n %}
{% block doc_content %}
{% if user.is_authenticated %}
<div class="container">
<div class="row" style="margin-top:10px;margin-bottom:10px;">
    <div class="col-md-2">
       <span class="btn btn-success fileinput-button">
            <i class="glyphicon glyphicon-plus"></i>
            <span>{% blocktrans %} Upload files {% endblocktrans %} </span>
            <input id="fileupload" type="file" name="file" multiple>
        </span>
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
            <tbody>
                {% for doc in docs %}
                    <tr>
                    {%  if doc.fiscal_id %}
                        <td>{{ doc.fiscal_id }}</td>
                    {% else %}
                        <td></td>
                    {%  endif %}
                    <td><a id="{{ doc.id }}" class="img_modal" data-id="{{ doc.id }}" data-toggle="modal" data-target="#myModal">{{ doc.name }}</a></td>
                    <td>{% if doc.date.day < 10%}0{% endif %}{{ doc.date.day }}/{% if doc.date.month < 10%}0{% endif %}{{ doc.date.month }}/{{ doc.date.year }}</td>
                    {%  if  doc.description %}
                        <td>{{ doc.description }}</td>
                    {%  else  %}
                        <td></td>
                    {%  endif %}
                    {%  if doc.lock %}
                        <td><span class="glyphicon glyphicon-lock"></span></td>
                    {%  else %}
                    <td></td>
                    {%  endif %}
                    {%  if doc.complete %}
                    <td><a id="btn_sp_{{ doc.id }}" class="btn btn-xs btn-default split_modal" data-id="{{ doc.id }}" title="Split" data-toggle="modal" data-target="#modal_split"><span class="glyphicon glyphicon-resize-full"></span></a>
                        <a id="btn_me_{{ doc.id }}" class="btn btn-xs btn-default merge_modal" data-id="{{ doc.id }}" title="Merge" data-toggle="modal" data-target="#modal_merge"><span class="glyphicon glyphicon-resize-small"></span></a>
                        <a id="btn_mv_{{ doc.id }}" class="btn btn-xs btn-default move_modal" data-id="{{ doc.id }}" title="Move" data-toggle="modal" data-target="#modal_move"><span class="glyphicon glyphicon-transfer"></span></a>
                        <a id="btn_dl_{{ doc.id }}" class="btn btn-xs btn-default download" data-id="{{ doc.id }}" title="Download"><span class="glyphicon glyphicon-download-alt"></span></a>
                        <a id="btn_de_{{ doc.id }}" class="btn btn-xs btn-default del_modal" data-id="{{ doc.id }}" title="Delete"><span class="glyphicon glyphicon-remove"></span></a></td>
                    {%  else %}
                    <td><a class="btn btn-xs btn-default"><span class="glyphicon glyphicon-refresh"></span> </a></td>
                    {%  endif %}
                </tr>
                {% endfor %}
            </tbody>
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
                        <select id="dlb_documents" name="dlb_documents" multiple="multiple" data-title="documents" data-source=""  data-value="index" data-text="name"></select>
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
</div>
{%  endif %}
{% endblock %}

{% block js %}
{% if user.is_authenticated %}
<script>
$(document).ready(function() {
    var datatable = $('#datatable').DataTable( {
            "language": {
                "url": "/static/datatables/i18n/{{ LANGUAGE_CODE }}.lang"
            }
        } );
});
</script>
{%  endif %}
{% endblock %}
