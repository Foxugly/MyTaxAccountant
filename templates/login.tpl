{% extends "layout.tpl" %}
{% load static %}
{% block content %}
{% if next %}
    {% if user.is_authenticated %}
    <p>Your account doesn't have access to this page. To proceed,
    please login with an account that has access.</p>
    {% else %}
    {% endif %}
{% endif %}
<div class="row">
  <div class="col-md-6 col-md-offset-3">
    <p><img style="display: block; margin-left: auto; margin-right: auto;" src=" {% static "logo_lieutenant_guillaume.png" %}"/></p>
    <form class="form-horizontal" method="post" action="{% url 'login' %}">
      {% csrf_token %}
      <fieldset>
        <!-- Form Name -->
        <legend><h1>Authentification</h1></legend>

        {% if form.errors %}
        <div class="alert alert-danger" role="alert">Your username and password didn't match. Please try again</div>
    {% endif %}

        <!-- Text input-->
        <div class="form-group">
          <label class="col-md-4 control-label" for="textinput">{{ form.username.label_tag }}</label>  
          <div class="col-md-4">{{ form.username }}</div>
        </div>

        <!-- Password input-->
        <div class="form-group">
          <label class="col-md-4 control-label" for="passwordinput">{{ form.password.label_tag }}</label>
          <div class="col-md-4">{{ form.password }}</div>
        </div>
        {% if next %}
          <input type="hidden" name="next" value="{{ next }}" />
        {% else %}
          <input type="hidden" name="next" value="/" />
        {% endif %}
        <!-- Button -->
        <div class="form-group">
          <label class="col-md-4 control-label" for="submit"></label>
          <div class="col-md-4">
            <input type="submit" class="btn btn-primary" value="login" />
          </div>
        </div>
      </fieldset>
    </form>
  </div>
</div>


{% endblock %}

