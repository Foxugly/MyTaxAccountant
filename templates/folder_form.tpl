{% extends "folder.tpl" %}
{% load staticfiles %}
{% load favorite %}
{% load upload_tags %}
{% load details_cat %}
{% load tools %}
{% load i18n %}
{% block doc_content %}
{% if user.is_authenticated %}
<div id="div_img_form" >
    <div id="div_img" class="col-md-9 h-scroll">
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
                var viewer= new Viewer(pictures);
        };
            </script>
    <div class="col-md-3">
        <div id="div_info" width="100%" style="min-height:55px;">
            <div id="alert_save_saved" class="alert alert-success" role="alert">{% blocktrans %} Saved !{% endblocktrans %}</div>
            <div id="alert_save_error" class="alert alert-danger" role="alert"></div>
        </div>
        <script>
             $('#alert_save_saved').hide();
             $('#alert_save_error').hide()
        </script>
        <div id="div_form" width="100%">
            <form class="form-horizontal">
                <fieldset>
                    <legend>{% blocktrans %} Document {% endblocktrans %}</legend>
                    <input id="doc_id" type="hidden" name="doc_id" value="{{ doc_id }}">
                    {{ doc_form.as_p }}
                </fieldset>
            </form>
        </div>
        <div id="div_btn_save">
            <div class="btn-group btn-group-justified">
                <a id="btn_save" class="btn btn-success">{% blocktrans %} Save {% endblocktrans %}</a>
                <a id="btn_save_next" class="btn btn-success">{% blocktrans %} Save and Next {% endblocktrans %}</a>
            </div>
        </div>
        <div id="div_pager" width="100%" style="text-align:center;">
            <p id="pagination"></p>
        </div>
        <script>
               $('#pagination').bootpag({
            total: {{ n_max }},
            page: {{ n_cur }},
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
            var pathname = window.location.pathname; // Returns path only
            var parts = pathname.split('/');
            var transfer = parts[0] + '/' + parts[1] + '/' + parts[2] + '/' + parts[3] + '/' + parts[4] + '/' + parts[5] + '/' + (num) + '/';
            console.log(transfer);
            window.location.replace(transfer);

        });
        </script>
    </div>
</div>

{%  endif %}
{% endblock %}

{% block js %}
<script src="{% static "viewer/viewer.min.js"%}"></script>
<script src="{% static "viewer/main.js"%}"></script>
{% endblock %}
