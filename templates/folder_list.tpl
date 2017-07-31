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
                    <th><input name="select_all" value="1" id="select-all" type="checkbox" /></th>
                    <th>{% trans "Fiscal ID" %}</th>
                    <th>{% trans "Document ID" %}</th>
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
                    <td></td>
                    <td>{%  if doc.fiscal_id %}{{ doc.fiscal_id }}{% endif %}</td>
                    <td>{{ doc.id }}</td>
                    <td><a id="{{ doc.id }}" class="img_modal" data-id="{{ doc.id }}" data-toggle="modal" data-target="#myModal">{{ doc.name }}</a></td>
                    <td>{% if doc.date.day < 10%}0{% endif %}{{ doc.date.day }}/{% if doc.date.month < 10%}0{% endif %}{{ doc.date.month }}/{{ doc.date.year }} {% if doc.date.hour < 10%}0{% endif %}{{ doc.date.hour }}:{% if doc.date.minute < 10%}0{% endif %}{{ doc.date.minute }}</td>
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
                    <td><a id="btn_vi_{{ doc.id }}" class="btn btn-xs btn-default view_modal" data-id="{{ doc.id }}" title="View"><span class="glyphicon glyphicon-file"></span></a>
                        <a id="btn_sp_{{ doc.id }}" class="btn btn-xs btn-default split_modal" data-id="{{ doc.id }}" title="Split" data-toggle="modal" data-target="#modal_split"><span class="glyphicon glyphicon-resize-full"></span></a>
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
                    <th><input name="select_all" value="1" id="select-all" type="checkbox" /></th>
                    <th>{% trans "Fiscal ID" %}</th>
                    <th>{% trans "Document ID" %}</th>
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
                <button id="document_multiple_move" type="button" class="btn btn-primary" data-dismiss="modal">{% trans "Move" %}</button>
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
                <div id="modal_pager" style="text-align:center;width:100%;">
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
<script type="text/javascript">


$(document).ready(function() {
    var rows_selected = [];
    var dict = {};
    var datatable = $('#datatable').DataTable( {
        'dom':
			"<'row'<'col-sm-4'l><'col-sm-4'B><'col-sm-4'f>>" +
			"<'row'<'col-sm-12'tr>>" +
			"<'row'<'col-sm-5'i><'col-sm-7'p>>",
            'buttons': [
                {  text: '<a id="btn_mv_selected" style="text-decoration: none;color:black;" data-toggle="modal" data-target="#modal_move"><span class="glyphicon glyphicon-transfer" title="{% trans "Transfer" %}"></span></a>',
                    action: function ( e, dt, node, config ) {
                        console.log("before");
                        var url = "/document/ajax/move/" + rows_selected[0] + "/";
                            console.log(url);
                        $("#document_move").hide();
                        $("#document_multiple_move").show();
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

                        console.log(rows_selected);
                        console.log("after");
                    }
                },
                {   text: '<span class="glyphicon glyphicon-download-alt " title="{% trans "Download" %}"></span>',
                    action: function () {
                        var url = '/document/ajax/multiple_download/';
                            console.log("download");
                            console.log(url);
                        for (var a=0; a < rows_selected.length;a++){dict[a] = rows_selected[a];}
                        $.ajax({
                            url: url,
                            dataType: "json",
                            data: dict,
                            success: function(result){
                                if (result["valid"]) {
                                    //window.open(result['url'], '_blank');
                                    //TODO
                                }
                            },
                            error: function(){
                                bootbox.alert("[download] ERROR with " + url);
                                return 0;
                            },
                        });
                    }
                },
                {  text: '<span class="glyphicon glyphicon-remove" title="{% trans "Delete" %}"></span>',
                    action: function () {
                        bootbox.confirm({
                            message: "Do you really want to delete selected document(s) ?",
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
                                    for (var a=0; a < rows_selected.length;a++){dict[a] = rows_selected[a];}
                                    $.ajax({
                                        type: "GET",
                                        contentType: "application/json",
                                        url : "/document/ajax/multiple_delete/",
                                        data: dict,
                                        dataType: "json",
                                        success: function(){
                                            window.location.reload();
                                        },
                                        error: function(){
                                            bootbox.alert("[del_modal] ERROR with " + url);
                                            return 0;
                                        },
                                    });
                                }
                            }
                        });
                   }
                }
            ],
        'language': {
            "url": "//cdn.datatables.net/plug-ins/1.10.13/i18n/French.json"
                    /* https://cdn.datatables.net/plug-ins/1.10.13/i18n/Dutch.json
                        https://cdn.datatables.net/plug-ins/1.10.13/i18n/English.json
                    {% with 'datatables/i18n/'|add:LANGUAGE_CODE|add:'.lang' as lang_url %}"{% static lang_url %}"{% endwith %}*/
        },
        'columnDefs': [
            {   targets: 0, searchable:false, orderable:false, className: 'dt-body-center',
                'render': function (data, type, full, meta){
                return '<input class="select-checkbox" type="checkbox" name="select-id[]" value="' + $('<div/>').text(data).html() + '">';
                }
            },
            { targets: 1, orderable : true },
            { targets: 2, orderable: true, visible: false },
            { targets: 3, orderable: true},
            { targets: 4, orderable: true, type: "date-euro" },
            { targets: 5, orderable: true },
            { targets: 6, orderable: true }
        ],
        select: {
            style:    'os',
            selector: 'td:first-child'
        },
        'order': [[4, 'asc']]
    });

    $('#datatable').on('click', 'input[type="checkbox"]', function(e){
        var $row = $(this).closest('tr');
        var data = datatable.row($row).data();
        var rowId = data[2];
        var index = $.inArray(rowId, rows_selected);
        if(this.checked && index === -1){
            rows_selected.push(rowId);
        } else if (!this.checked && index !== -1){
            rows_selected.splice(index, 1);
        }
        if(this.checked){
            $row.addClass('selected');
        } else {
            $row.removeClass('selected');
        }
        e.stopPropagation();
    });

    // Handle click on table cells with checkboxes --- tbody td,
    $('#datatable').on('click', 'thead th:first-child', function(e){
      $(this).parent().find('input[type="checkbox"]').trigger('click');
    });

    // Handle click on "Select all" control
    $('#datatable thead input[name="select_all"]', datatable.table().container()).on('click', function(e){
        if(this.checked){
            $('#datatable tbody input[type="checkbox"]:not(:checked)').trigger('click');
        } else {
            $('#datatable tbody input[type="checkbox"]:checked').trigger('click');
        }
        e.stopPropagation();
    });

    $('#select-all').on('click', function(){
      // Check/uncheck all checkboxes in the table
      var rows = datatable.rows({ 'search': 'applied' }).nodes();
      $('input[type="checkbox"]', rows).prop('checked', this.checked);
    });

    $('#document_multiple_move').click(function document_move(){
        var url = "/document/ajax/multiple_move/" + $("#modal_category").val() + "/";
        for (var a=0; a < rows_selected.length;a++){dict[a] = rows_selected[a];}
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            data: dict,
            dataType: 'json',
            success: function() {
                window.location.reload();
            },
            error: function(){
                bootbox.alert("[click on document_move] ERROR with " + url);
                return 0;
            },
        });
    });
    $('.view_modal').click(function(e) {
        var pathname = window.location.pathname; // Returns path only
        var parts = pathname.split('/');
        var field = $('#datatable').dataTable().fnSettings().aaSorting[0][0];
        var sens = $('#datatable').dataTable().fnSettings().aaSorting[0][1];
        var n_in_page = $(this).closest('tr').index() + 1;
        var n_length_page = $('#datatable').DataTable().page.info().length;
        var n_current_page = $('#datatable').DataTable().page.info().page;
        var n = (n_length_page * n_current_page) + n_in_page;
        var url = parts[0] + '/' + parts[1] + '/' + parts[2] + '/form/' + field + '/' + sens + '/' + n + '/';
        console.log(url);
        window.location.replace(url);
    });
});

</script>
{%  endif %}
{% endblock %}
