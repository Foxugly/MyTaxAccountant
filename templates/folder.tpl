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
        <div class="col-md-10">
            <ul class="nav nav-tabs nav-pills" role="tablist">
                {% for c in categories %}
                    {%if c == category_current %}
                        <li class="active"><a id="{{c.id}}" data-id="{{c.id}}" href="/category/{{c.id}}/">{{c.cat.name}} <span class="badge">{{c|len_docs}}</span></a></li>
                    {% else %}
                        <li><a id="{{c.id}}" data-id="{{c.id}}" href="/category/{{c.id}}/">{{c.cat.name}} <span class="badge">{{c|len_docs}}</span></a></li>
                    {% endif %}
                {% endfor %}
            </ul>
        </div>
        <div class="col-md-2 text-right">
            <div id="view_group" class="btn-group" data-toggle="buttons">
                <label id="btn_view_list" class="btn btn-default {%  if view == 'list' %}active{%  endif %}">
                    <input id="input_view_list" name="view_data" value="list" type="radio"><span class="glyphicon glyphicon-list"></span>
                </label>
                <label id="btn_view_form" class="btn btn-default {%  if view == 'form' %}active{%  endif %}">
                    <input id="input_view_form" name="view_data" value="form" type="radio"><span class="glyphicon glyphicon-file"></span>
                </label>
            </div>
            <script>
                $("#btn_view_form").click(function () {
                    var pathname = window.location.pathname; // Returns path only
                    var parts = pathname.split('/');
                    var field = $('#datatable').dataTable().fnSettings().aaSorting[0][0];
                    var sens = $('#datatable').dataTable().fnSettings().aaSorting[0][1];
                    var transfer = parts[0] + '/' + parts[1] + '/' + parts[2] + '/form/' + field + '/' + sens + '/1/';
                    console.log($('#datatable').dataTable().fnSettings());
                    console.log(transfer);
                    window.location.replace(transfer);
                });
                $("#btn_view_list").click(function () {
                    var pathname = window.location.pathname; // Returns path only
                    var parts = pathname.split('/');
                    var transfer = parts[0] + '/' + parts[1] + '/' + parts[2] + '/' ;
                    console.log(transfer);
                    window.location.replace(transfer);
                });
            </script>
        </div>
    </div>
{% block doc_content %}
{% endblock %}
    {%  endif %}
{% endblock %}

