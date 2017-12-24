{% extends "layout.tpl" %}
{% load bootstrap3 %}
{% load staticfiles %}
{% load favorite %}
{% load upload_tags %}
{% load details_cat %}
{% load tools %}
{% load i18n %}

{% block content %}
{% if user.is_superuser %}
{%  if templatetrimester_return %}
<div class="row">
    <div class="col-md-10 col-md-offset-1">
        <div class="alert alert-success" role="alert">Template trimester added !</div>
    </div>
</div>
{%  endif %}
{%  if fiscalyear_return %}
<div class="row">
    <div class="col-md-10 col-md-offset-1">
        <div class="alert alert-success" role="alert">Fiscal year added !</div>
    </div>
</div>
{%  endif %}
    {%  if trimesters_return %}
<div class="row">
    <div class="col-md-10 col-md-offset-1">
        <div class="alert alert-success" role="alert">Trimester added !</div>
    </div>
</div>
{%  endif %}
<div class="row">
    <div class="col-md-5 col-md-offset-1">
        <div class="panel panel-primary">
            <div class="panel-heading">List of fiscal years </div>
            <div class="panel-body">
                <table class="table table-bordered">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Init</th>
                        <th>Favorite</th>
                  </tr>
                </thead>
                <tbody>
                {%  for fy in fiscalyears %}
                  <tr>
                    <td>{{ fy.id }}</td>
                    <td>{{ fy.name }}</td>
                    <td>{% if fy.init %}<span class="glyphicon glyphicon-ok" aria-hidden="true"></span>{% endif %}</td>
                    <td>{% if fy.favorite %}<span class="glyphicon glyphicon-ok" aria-hidden="true"></span>{% endif %}</td>
                  </tr>
                {%  endfor %}
                </tbody>
              </table>
            </div>
        </div>
    </div>
    <div class="col-md-5">
        <div class="panel panel-primary">
            <div class="panel-heading">New fiscal year </div>
            <div class="panel-body">
                <form class="form-horizontal" method="post" action="{{fiscalyear_url}}">
                    <input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">
                    {% bootstrap_form fiscalyear_form layout="horizontal"%}
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
<div class="row">
    <div class="col-md-5 col-md-offset-1">
        <div class="panel panel-primary">
            <div class="panel-heading">List of trimester templates </div>
            <div class="panel-body">
                <table class="table table-bordered">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>year</th>
                        <th>number</th>
                        <th>favorite</th>
                        <th>start_date</th>
                    </tr>
                </thead>
                <tbody>
                {%  for tt in templatetrimesters %}
                    <tr>
                        <td>{{ tt.id }}</td>
                        <td>{{ tt.year }}</td>
                        <td>{{ tt.number }}</td>
                        <td>{% if tt.favorite %}<span class="glyphicon glyphicon-ok" aria-hidden="true"></span>{% endif %}</td>
                        <td>{{ tt.start_date }}</td>
                    </tr>
                {%  endfor %}
                </tbody>
              </table>
                <a href="/utils/add_trimesters/" class="btn btn-block btn-lg btn-info"><span class="glyphicon glyphicon-calendar"></span> Add trimester to all companies from favorite trimester template</a>
            </div>
        </div>
    </div>
    <div class="col-md-5">
        <div class="panel panel-primary">
            <div class="panel-heading">New trimester template </div>
            <div class="panel-body">
                <form class="form-horizontal" method="post" action="{{templatetrimester_url}}">
                    <input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">
                    {% bootstrap_form templatetrimester_form layout="horizontal"%}
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
