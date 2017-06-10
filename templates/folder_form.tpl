{% extends "folder.tpl" %}
{% load staticfiles %}
{% load favorite %}
{% load upload_tags %}
{% load details_cat %}
{% load tools %}
{% load i18n %}
{% block doc_content %}
{% if user.is_authenticated %}
<div id="div_img_form" class="row">
    <div id="div_img" class="col-md-9 docs-galley" style="overflow-y: auto; text-align:center;">
        <ul class="docs-pictures clearfix">
             {% autoescape off %}
			{{ img }}
            {% endautoescape %}
		</ul>
    </div>
<script>
       window.onload = function () {
  'use strict';
        var Viewer = window.Viewer;
        var pictures = document.querySelector('.docs-pictures');
        var viewer;
        viewer = new Viewer(pictures);
};
    </script>
    <div class="col-md-3">
        <div id="div_info" width="100%" style="min-height:55px;">
            <div id="alert_save_saved" class="alert alert-success" role="alert">{% blocktrans %} Saved !{% endblocktrans %}</div>
            <div id="alert_save_error" class="alert alert-danger" role="alert"></div>
        </div>
        <div id="div_form" width="100%">{{ doc_form | escape }}</div>
        <div id="div_pager" width="100%" style="text-align:center;">
            <p id="pagination"></p>
        </div>
    </div>
</div>

{%  endif %}
{% endblock %}

{% block js %}
<script src="{% static "viewer/viewer.min.js"%}"></script>
<script src="{% static "viewer/main.js"%}"></script>

{% endblock %}
