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
<div class="row">
    <div class="col-md-12">
        {%  if return %}
        <div class="alert alert-success" role="alert">User and company added</div>
        {%  endif %}
        <form class="form-horizontal" method="post" action="{{url}}">
        <input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">
        {%  for f in form %}
           <!-- {% bootstrap_form f layout="horizontal"%} -->
           {% for field in form %}
              <div class="form-group">
                    <label {% if field.required %}class="col-md-3 control-label required" {% else %}class="col-md-3 control-label" style="font-weight: normal !important;"{% endif %} for="{{field.label_tag}}">
                    {% bootstrap_label field.label %}
                 </label>
                 <div class="col-md-9">{% bootstrap_field field show_label=False %}</div>
              </div>
           {% endfor %}
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
    <!--
<div class="row">
    <div class="col-md-12">
        <table id="datatable" class="table table-striped table-bordered" width="100%" cellspacing="0">
            <thead>
                <tr>
                    <th>{% trans "FiscalID" %}</th>
                    <th>{% trans "Name" %}</th>
                    <th>{% trans "Date" %}</th>
                    <th>{% trans "Comments" %}</th>
                    <th>{% trans "Lock" %}</th>
                    <th>{% trans "Operations" %}</th>
                </tr>
            </thead>
     
            <tfoot>
                <tr>
                    <th>{% trans "FiscalID" %}</th>
                    <th>{% trans "Name" %}</th>
                    <th>{% trans "Date" %}</th>
                    <th>{% trans "Comments" %}</th>
                    <th>{% trans "Lock" %}</th>
                    <th>{% trans "Operations" %}</th>
                </tr>
            </tfoot>
     
            <tbody>
            </tbody>
        </table>
    </div>
</div> -->
{%  endif %}
{% endblock %}

{% block js %}
<script>
$(document).ready(function() {
    var datatable = $('#datatable').DataTable();
});
</script>
{% endblock %}
