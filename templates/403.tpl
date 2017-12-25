{% extends "layout2.tpl" %}
{% load bootstrap3 %}
{% load i18n %}
{% block content %}
<div class="container">
    <div class="row">
        <div class="col-md-10 col-md-offset-1">
            <div class="panel panel-warning">
                <div class="panel-heading">{% trans 'Forbidden Acces' %}</div>
                <div class="panel-body">{% trans "We are sorry, but you can not have access to this page." %}</div>
            </div>
        </div>
    </div>
</div>
{% endblock %}