{% extends "base.tpl" %}
{% load bootstrap3 %}
{% load i18n %}
{% block content %}
<div class="container">
    <div class="row">
        <div class="col-md-10 col-md-offset-1">
            <div class="panel panel-error">
                <div class="panel-heading">{% trans '500 Server Error' %}</div>
                <div class="panel-body">{% trans "Internal error." %}</div>
            </div>
        </div>
    </div>
</div>
{% endblock %}