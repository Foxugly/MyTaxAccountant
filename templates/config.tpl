{% extends "layout.tpl" %}
{% load bootstrap3 %}
{% load i18n %}
{% load l10n %}
{% load tools %}
{% load static %}


{% block js %}
<script>
$(document).ready(function() {

    $('.datepicker').datetimepicker({
        locale: '{{ LANGUAGE_CODE }}',
        format: 'L'
    });

    $('.btn_company').click(function(){
        var f = this.id.replace("btn", "form");
        var id = this.id.split('_')[2];
        var form = $('#' + f);
        var url = '/company/ajax/update/' + id + '/';
        $.ajax({
            url: url,
            type: 'POST',
            data: form.serialize(),
            traditional: true,
            dataType: 'json',
            success: function (result) {
                if (result['return']){
                    $('#div_change_business_data_'+id).html('<div class="alert alert-success" role="alert">Data changed !</div>');
                    $('#div_change_business_data_'+id).show().delay( 1000 ).fadeOut(1000);
                }
                else{
                    var out = '';
                    for (var key in result['errors']){
                        out += result['errors'][key][0] + '<br>';
                    }
                    $('#div_change_business_data_'+id).html('<div class="alert alert-danger" role="alert">' + out + '</div>');
                    $('#div_change_business_data_'+id).show();
                }
            }
        });
    });

    $('#btn_personal_data').click(function(){
        var form = $('#form_personal_data');
        var url = '/user/ajax/personal_data/';
        $.ajax({
            url: url,
            type: 'POST',
            data: form.serialize(),
            traditional: true,
            dataType: 'json',
            success: function(result){
                if (result['return']){
                    $('#div_change_personal_data').html('<div class="alert alert-success" role="alert">Personal data changed !</div>');
                    $('#div_change_personal_data').show().delay( 1000 ).fadeOut(1000);
                }
                else{
                    var out = '';
                    for (var key in result['errors']){
                        out += result['errors'][key][0] + '<br>';
                    }
                    $('#div_change_personal_data').html('<div class="alert alert-danger" role="alert">' + out + '</div>');
                    $('#div_change_personal_data').show();
                }
            }
        });
    });


    $('#btn_password').click(function(){
        var form = $('#form_password');
        var url = '/user/ajax/password/';
        $.ajax({
            url: url,
            type: 'POST',
            data: form.serialize(),
            traditional: true,
            dataType: 'json',
            success: function(result){
                if (result['return']){
                    $('#id_old_password').val('');
                    $('#id_new_password1').val('');
                    $('#id_new_password2').val('');
                    $('#div_change_pwd').html('<div class="alert alert-success" role="alert">Password changed !</div>');
                    $('#div_change_pwd').show().delay( 1000 ).fadeOut(1000);
                }
                else{
                    var out = '';
                    for (var key in result['errors']){
                        out += result['errors'][key][0] + '<br>';
                    }
                    $('#div_change_pwd').html('<div class="alert alert-danger" role="alert">' + out + '</div>');
                    $('#div_change_pwd').show();
                }
            },
        error: function() {
          alert("There was an error. Try again please!");
        }
        });
    });
});
</script>
{% endblock %}

{% block content %}
<div class="container">
    <h2>{% trans "Configuration and Settings" %}</h2>
    <ul class="nav nav-tabs">
        <li class="active"><a data-toggle="tab" href="#div_personal_data">{% trans "Personal Data" %}</a></li>
        <li><a data-toggle="tab" href="#div_business">{% trans "Business Data" %}</a></li>
        <li><a data-toggle="tab" href="#div_password">{% trans "Password" %}</a></li>
    </ul>

    <div class="tab-content">
        <div id="div_personal_data" class="tab-pane in active">
             <div class="row row_space">
                <div id="div_change_personal_data"> </div>
                <form class="form-horizontal" id="form_personal_data" >
                    {% csrf_token %}
                    <fieldset>
                        <div class="row">
                            {% bootstrap_form user_form layout="horizontal"%}
                            {% bootstrap_form userprofile_form layout="horizontal"%}
                        </div>
                        <div class="row">
                            <div class="form_group">
                                <div class="col-md-9 col-md-offset-3">
                                    <a href="#" id="btn_personal_data" class="btn btn-primary"> Submit</a>
                                </div>
                            </div>
                        </div>
                    </fieldset>
                </form>
            </div>
        </div>

        <div id="div_business" class="tab-pane">
            <div class="row row_space">
                <ul class="nav nav-tabs">
                    {%  for comp in companies %}
                        {% if forloop.first %}
                            <li class="active"><a data-toggle="tab" data-id="{{ comp.id }}" href="#company_{{ comp.id }}">{{ comp }}</a></li>
                        {%  else %}
                            <li><a data-toggle="tab" data-id="{{ comp.id }}" href="#company_{{ comp.id }}">{{ comp }}</a></li>
                        {%  endif %}
                    {%  endfor %}
                </ul>
                <div class="tab-content">
                        {% for id, compF in companiesForm%}
                            {% if forloop.first %}
                                <div id="company_{{ id }}" class="tab-pane in active">
                            {%  else %}
                                <div id="company_{{ id }}" class="tab-pane">
                            {%  endif %}
                                <div class="row row_space">
                                    <div id="div_change_business_data_{{ id }}"> </div>
                                   <form class="form-horizontal" id= "form_company_{{ id }}">
                                        {% bootstrap_form compF layout="horizontal"%}
                                    </form>
                                </div>
                                <div class="row">
                                    <div class="form_group">
                                        <div class="col-md-9 col-md-offset-3">
                                            <a href="#" id="btn_company_{{ id }}" class="btn btn-primary btn_company"> Submit</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        {% endfor %}
                </div>
            </div>
        </div>

        <div id="div_password" class="tab-pane">
            <div class="row row_space">
                <div id="div_change_pwd"> </div>
                <form class="form-horizontal" id="form_password">
                    {% csrf_token %}
                    <fieldset>
                        <div class="row">
                            {% bootstrap_form password_change_form layout="horizontal"%}
                        </div>
                        <div class="row">
                            <div class="form_group">
                                <div class="col-md-9 col-md-offset-3">
                                    <a href="#" id="btn_password" class="btn btn-primary"> Submit</a>
                                </div>
                            </div>
                        </div>
                    </fieldset>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}