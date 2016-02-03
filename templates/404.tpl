{% extends "layout.tpl" %}
{% load bootstrap3 %}
{% load i18n %}
{% block content %}
<div class="alert alert-danger" role="alert"><b>404</b> {% blocktrans %}Missing page{% endblocktrans %}</div>
{% endblock %}