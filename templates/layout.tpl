{% extends "base.tpl" %}
{% load bootstrap3 %}
{% load i18n %}
{% load favorite %}
{% load static %}
{% load hijack_tags %}

{% block navigation %}
  <form class="navbar-form navbar-left" role="search">
    <div class='form-group'>
      <select id="sel_company" class="form-control  select2-nosearch" >
        <optgroup label = "{% blocktrans %}Choose a company{% endblocktrans %}">
          {% for c in companies %}
            {% if  c == company_current %}
              <option value='{{c.id}}' selected>{{ c|name }}</option>
            {% else %}
              <option value='{{c.id}}'>{{ c|name }}</option>
            {% endif %}
          {% endfor %}
        </optgroup>
      </select>
    </div>
      <div class='form-group'>
        <select id="sel_year" class="form-control  select2-nosearch" style="width:200px;">
            <optgroup label = "{% blocktrans %}Choose a fiscal year{% endblocktrans %}">
          {% for y in years %}
            {% if  y == year_current %}
              <option value='{{y.id}}' selected>{{ y|name }}</option>
            {% else %}
              <option value='{{y.id}}'>{{ y|name }}</option>
            {% endif %}
          {% endfor %}
        </optgroup>
        </select>
      </div>
      <div class='form-group'>
        <select id="sel_trimester" class="form-control  select2-nosearch" style="width:200px;">
            <optgroup label = "{% blocktrans %}Choose a trimester{% endblocktrans %}">
          {% for t in trimesters %}
            {% if  t == trimester_current %}
              <option value='{{t.id}}' selected>{{ t|name }}</option>
            {% else %}
              <option value='{{t.id}}'>{{ t|name }}</option>
            {% endif %}
          {% endfor %}
        </optgroup>
        </select>
      </div>
  </form>
{%  endblock %}