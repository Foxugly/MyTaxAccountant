{% comment %}

# Copyright 2011, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

{% endcomment %}
{% load bootstrap3 %}
{% load i18n %}
{% load favorite %}
{% load staticfiles %}
{% load hijack_tags %}
<!DOCTYPE HTML>
<html lang="en">
  <head>
    <title>MyLieutenantGuillaume</title>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
    <!--  CSS -->

    <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="{% static 'hijack/hijack-styles.css' %}" />
    <link rel="stylesheet" href="https://cdn.datatables.net/1.10.9/css/dataTables.bootstrap.min.css">
    <link rel="stylesheet" href=" {% static "upload/css/style.css" %} ">
    <link rel="stylesheet" href=" {% static "upload/css/jquery.fileupload-ui.css" %}" >
    <link rel="stylesheet" href='{% static "select2-4.0.1/dist/css/select2.min.css" %}'  />
    <link rel="stylesheet" href='{% static "bootstrap-datetimepicker-master/build/css/bootstrap-datetimepicker.min.css" %}' />
    <link rel="stylesheet" href="{% static "viewer/viewer.min.css"%}">
    {% block css %}
    {% endblock %}
    <link href='{% static "css/perso.css" %}' rel='stylesheet' />
    <!--  JS -->
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
    <script type="text/javascript" src="https://momentjs.com/downloads/moment-with-locales.js"></script>
    <script type="text/javascript" src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/1.10.9/js/jquery.dataTables.js"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/1.10.9/js/dataTables.bootstrap.min.js"></script>
    <script type="text/javascript" src=" {% static "upload/js/vendor/jquery.ui.widget.js" %}"></script>
    <script type="text/javascript" src=" {% static "upload/js/jquery.iframe-transport.js" %}"></script>
    <script type="text/javascript" src=" {% static "upload/js/jquery.fileupload.js" %}"></script>
    <script type="text/javascript" src=" {% static "upload/js/jquery.cookie.js" %}"></script>
    <script type="text/javascript" src=" {% static "bootpag/jquery.bootpag.min.js" %}"></script>
    <script type="text/javascript" src=" {% static "bootbox/bootbox.min.js" %}"></script>
    <script type="text/javascript" src='{% static "select2-4.0.1/dist/js/select2.min.js" %}'></script>
    {% if LANGUAGE_CODE != 'en' %}
        {% with 'select2-4.0.1/dist/js/i18n/'|add:LANGUAGE_CODE|add:'.js' as select2_lang %}
        <script type="text/javascript" src='{% static select2_lang %}'></script>
        {% endwith %}
    {%  endif %}
    <script src='{% static "duallistbox/dual-list-box.min.js" %}'></script>

    <script type="text/javascript" src='{% static "bootstrap-datetimepicker-master/build/js/bootstrap-datetimepicker.min.js" %}'></script>

    <script src='{% static "viewer/viewer.min.js" %}'></script>
    <!--<script src='{% static "viewer/main.js" %}'></script>-->
    {% block js %}
    {% endblock %}
    {% block header %}
    {% endblock %}
  </head>
  <body>
  {% hijack_notification %}
    <nav class="navbar navbar-fixed-top navbar-inverse">
      <div class="container-fluid">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="/"><span class="glyphicon glyphicon-home"> MyLieutenantGuillaume</span></a>
        </div>
        <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
          {% if user.is_authenticated %}
          <form class="navbar-form navbar-left" role="search">
            <div class='form-group'>
              <select id="sel_company" class="form-control  select2-nosearch" >
                <optgroup label = "Choose a company">
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
                    <optgroup label = "Choose a company">
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
                    <optgroup label = "Choose a company">
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
              {% if user.is_superuser %}
              <ul class="nav navbar-nav navbar-left">
                <li class="dropdown">
                  <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false"><span class="glyphicon glyphicon-cog"></span><span class="caret"></span></a>
                  <ul class="dropdown-menu">
                    <li><a href="{%  url 'years' %}">{% blocktrans %} years{% endblocktrans %}</a></li>
                    <li><a href="{%  url 'trimesters' %}">{% blocktrans %} trimesters{% endblocktrans %} </a></li>
                    <li><a href="{%  url 'companies' %}">{% blocktrans %} companies{% endblocktrans %} </a></li>
                  </ul>
                </li>
              </ul>
                  {% endif %}
          {% endif %}

          <ul class="nav navbar-nav navbar-right">
            <li>
                <div class='navbar-form form-group'>
                    <select id="language" name="language" class="form-control select2-nosearch">
                        {% get_current_language as LANGUAGE_CODE %}
                        {% get_available_languages as LANGUAGES %}
                        {% get_language_info_list for LANGUAGES as languages %}
                        {% for language in languages %}
                            <option value="{{ language.code }}"{% if language.code == LANGUAGE_CODE %} selected="selected"{% endif %}>
                                {{ language.name_local|capfirst }}
                            </option>
                        {% endfor %}
                    </select>
                </div>
            </li>
            <li><a href="/">{% blocktrans %} Help{% endblocktrans %} </a></li>
            {% if user.is_authenticated %}
            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false"><span class="glyphicon glyphicon-user"></span> {{user.first_name}} {{user.last_name}} <span class="caret"></span></a>
              <ul class="dropdown-menu">
                <li><a class="glyphicon glyphicon-cog" href="{%  url 'settings' %}">{% blocktrans %} Profil{% endblocktrans %} </a></li>
                <li><a class="glyphicon glyphicon-off" href="{%  url 'logout' %}">{% blocktrans %} Déconnexion{% endblocktrans %} </a></li>
              </ul>
            </li>
            {% else %}
                <li><a href="{%  url 'login' %}">{% trans "Connexion" %}</a></li>
            {% endif %}
          </ul>
        </div>
      </div>
    </nav>
    {% block content %}
    <div class="container"><!--<div class="container-fluid">-->
        <!--[if lt IE 9]>
           	<div id="topwarning">
    		{% blocktrans %}
    		Warning ! You are using an outdated version of Internet Explorer !<br>
    		This website will <strong>NOT</strong> work with your version !
    		Please update to <a href="http://www.microsoft.com/france/windows/internet-explorer/telecharger-ie9.aspx#/top"> Internet Explorer 9</a> or to <a href="http://www.mozilla.org/fr/firefox/new/">Firefox</a>
    		or <a href="https://www.google.com/chrome?hl=fr">Chrome</a>
    		{% endblocktrans %}
    		</div>
    	<![endif]-->

      <div class='row'>
        
          {% if not user.is_authenticated %}
          	  <div class="col-md-6 col-md-offset-3" style="margin-top:20px"><p><img style="display: block; margin-left: auto; margin-right: auto;" src=" {% static "logo_lieutenant_guillaume.png" %}"/></p></div>
              <div class="col-md-6 col-md-offset-3" style="margin-top:20px">
                {% blocktrans %}
                <p>Nous avons développé un service cloud pour faire bénéficier nos clients d'un espace de stockage gratuit et centralisé.</p>
<p>Cet espace d’archivage est entièrement protégé et accessible 24h/24, 7j/7.</p>
<p>Au même moment, ce canal de communication entre votre exploitation et notre cabinet nous permet de faciliter la synchronisation de vos données.</p>
<p>En effet, dès que vos documents professionnels ont été numérisés et téléchargés par vos soins sur notre bureau virtuel, nous les traitons et vous soumettons un reporting mensuel.</p>
                {% endblocktrans %}
          	  </div>
              <div class="col-md-4 col-md-offset-4" style="margin-top:20px">
                <a href="{%  url 'login' %}" class="btn btn-success btn-lg btn-block">{% blocktrans %}Connexion{% endblocktrans %} </a>
              </div>
  	        </div>
          {% endif %}
      </div>
    </div>
  {% endblock %}
  </body>
  <script type="text/javascript" src='{% static "js/perso.js" %}'></script>
</html>
