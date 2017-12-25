{% extends "layout2.tpl" %}
{% load bootstrap3 %}
{% load staticfiles %}
{% load favorite %}
{% load upload_tags %}
{% load details_cat %}
{% load tools %}
{% load i18n %}

{% block content %}
{% if user.is_superuser %}
{%  if return %}
<div class="row">
    <div class="col-md-6 col-md-offset-3">
        <div class="alert alert-success" role="alert">User and company added</div>
    </div>
</div>
{%  endif %}
{%  if companies %}
<div class="row">
    <div class="col-md-6 col-md-offset-3">
        <div class="panel panel-primary">
            <div class="panel-heading">List of companies </div>
            <div class="panel-body">
                <table class="table table-bordered">
                <thead>
                    <tr>
                        <th>Name of company</th>
                        <th>Model trimester</th>
                        <th>Active</th>
                        <th>Last Trimester</th>
                  </tr>
                </thead>
                <tbody>
                {%  for c in companies %}
                    <tr>
                        <td>{{ c.name }}</td>
                        <td>{{ c.model_trimester }}</td>
                        <td>{% if c.active %}<span class="glyphicon glyphicon-ok" aria-hidden="true"></span>{% endif %}</td>
                        <td>{{ c | current_trimester }}</td>
                    </tr>
                {%  endfor %}
                </tbody>
              </table>
            </div>
        </div>
    </div>
</div>
{% endif %}
<div class="row">
    <div class="col-md-6 col-md-offset-3">
        <div class="panel panel-primary">
            <div class="panel-heading">New company and user</div>
            <div class="panel-body">
                <form class="form-horizontal" method="post" action="{{url}}">
                <input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">
                {%  for form in forms %}
                    {% bootstrap_form form layout="horizontal"%}
                {%  endfor %}
                <div class="row">
                    <div class="form_group">
                        <div class="col-md-9 col-md-offset-3">
                            <input type="submit" class="btn btn-primary" value="Add" />
                        </div>
                    </div>
                </div>
                </form>
            </div>
        </div>
    </div>
</div>
{%  endif %}
{% endblock %}

{% block js %}
<script>
$(document).ready(function() {
    var datatable = $('#datatable').DataTable();
    $('.datepicker').datetimepicker({
        locale: '{{ LANGUAGE_CODE }}',
        format: 'L'
    });
});
</script>
{% endblock %}
