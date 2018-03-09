{% extends "base.tpl" %}
{% load static %}
{% load favorite %}
{% load upload_tags %}
{% load details_cat %}
{% load tools %}
{% load i18n %}
{% block content %}
    {% if user.is_authenticated %}
    <div class="row">
        <div class="col-md-6 col-md-offset-3">
            <h2>{% blocktrans %}Tree of unlocked documents{%  endblocktrans %}</h2>
            <div id="treeview1" class=""></div>
        </div>
    </div>
    <script type="text/javascript">
    $(function() {
        var defaultData = [{% for l in tree %}  {{l|safe}}, {% endfor %}];
        $('#treeview1').treeview({
          enableLinks: true,
          showTags: true,
          data: defaultData,
          levels: 5
        }).treeview('collapseAll', { silent: true });
    });
    </script>
    {%  endif %}
{% endblock %}

