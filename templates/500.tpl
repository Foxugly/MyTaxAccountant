{% extends "layout.tpl" %}
{% load bootstrap3 %}
{% load i18n %}
{% block content %}
<div class="alert alert-danger" role="alert"><b>500</b> {% blocktrans %}server error{% endblocktrans %}</div>
{% endblock %}