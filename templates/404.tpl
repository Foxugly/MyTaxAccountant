{% extends "base.tpl" %}
{% load bootstrap3 %}
{% load i18n %}
{% block content %}
<div class="container">
    <div class="row">
        <div class="col-md-10 col-md-offset-1">
            <div class="panel panel-warning">
                <div class="panel-heading">{% trans 'Page not found' %}</div>
                <div class="panel-body">{% trans "We're sorry, but the requested page could not be found." %}</div>
            </div>
        </div>
    </div>
</div>
{% endblock %}