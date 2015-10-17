{% comment %}

# Copyright 2011, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

{% endcomment %}
{% load i18n %}
{% load favorite %}

<!DOCTYPE HTML>
<html lang="en">
  <head>
    <title>MyTaxAccountant</title>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
    <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
    {% block header %}
    {% endblock %}
  </head>
  <body>
    <nav class="navbar navbar-fixed-top navbar-inverse">
      <div class="container-fluid">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">MyTaxAccoutant</a>
        </div>
        {% if userprofile.user.is_authenticated %}
        <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
          <form class="navbar-form navbar-left" role="search">
            <div class='form-group'>
              <select id="sel_company" class="form-control" >
                  <optgroup label = "Choose a compagny">
                    {% for c in userprofile|companies %}
                      {% if company %}
                        {% if  c == company %}
                          <option value='{{c.id}}' selected>{{c.id}} {{ c|name }}</option>
                        {% else %}
                          <option value='{{c.id}}'>{{c.id}} {{ c|name }}</option>
                        {% endif %}
                      {% else %}
                        {% if  c == userprofile|favorite_company %}
                          <option value='{{c.id}}' selected>{{c.id}} {{ c|name }}</option>
                        {% else %}
                          <option value='{{c.id}}'>{{c.id}} {{ c|name }}</option>
                        {% endif %}
                      {% endif %}
                    {% endfor %}
                  </optgroup>
                </select>
              </div>
              <div class='form-group'>
                <select id="sel_year" class="form-control" >
                  <optgroup label = "Choose a tax year">
                    {% for y in userprofile|companies|years %}
                      {% if year %}
                        {% if y == trimester %}
                          <option value='{{y.id}}' selected>{{y.id}} {{ y }}</option>
                        {% else %}
                          <option value='{{y.id}}'>{{y.id}} {{ y }}</option>
                        {% endif %}
                      {% else %}
                        {% if y == userprofile|companies|favorite_year %}
                          <option  value='{{y.id}}' selected>{{y.id}} {{ y }}</option>
                        {% else %}
                          <option value='{{y.id}}'>{{y.id}} {{ y }}</option>
                        {% endif %}
                      {% endif %}
                    {% endfor %}
                  </optgroup>
                </select>
              </div>
              <div class='form-group'>
                <select id="sel_trimester" class="form-control" >
                  <optgroup label = "Choose a trimester">         
                    {% for t in userprofile|companies|years|trimesters %}
                      {% if trimister %}
                        {% if t == trimester %}
                          <option value='{{t.id}}' selected>{{t.id}} {{ t}}</option>
                        {% else %}
                          <option value='{{t.id}}'>{{t.id}} {{ t}}</option>
                        {% endif %}
                      {% else %}
                        {% if t == userprofile|companies|years|favorite_trimester %}
                          <option value='{{t.id}}' selected>{{t.id}} {{ t }}</option>
                        {% else %}
                          <option value='{{t.id}}'>{{t.id}} {{ t }}</option>
                        {% endif %}
                      {% endif %}
                    {% endfor %}
                  </optgroup>
                </select>
              </div>
          </form>
          <ul class="nav navbar-nav navbar-right">
            <li><a href="#">Help</a></li>
            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false"><span class="glyphicon glyphicon-user"></span> {{userprofile.user.first_name}} {{userprofile.user.last_name}} <span class="caret"></span></a>
              <ul class="dropdown-menu" style='background:black;color:white;'>
                <li><a class="glyphicon glyphicon-cog" href="/user/settings/"> Profil</a></li>
                <li><a class="glyphicon glyphicon-off" href="/user/logout/"> Déconnexion</a></li>
              </ul>
            </li>
          </ul>
        </div>
        {% endif %}
      </div>
    </nav>
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
    <div id="content">
      {% block info %}
      {% endblock %}
      {% block content %}
        {% if not userprofile.user.is_authenticated %}
          <div class="row">
        	  <div class="col-md-6 col-md-offset-3"><p><img style="display: block; margin-left: auto; margin-right: auto;" src="http://www.lieutenantguillaume.com/static/img/partner-of-success-stories.png"/></p>
            </div>
            <div class="col-md-6 col-md-offset-3">
              {% blocktrans %}
              <p>Lieutenant Guillaume proposes you the opportunity of uploading your invoices, tax documents, bank documents and other. This plateform guarantees the backup of your documents and simplifies the transfert of your document to Lieutenant Guillaume.</p>
              {% endblocktrans %}   
        	  </div>
            <div class="col-md-6 col-md-offset-3">
              <a href="/user/login" class="btn btn-success btn-lg btn-block">Connexion</a>
            </div>
	        </div>
        {% endif %}
      {% endblock %}
    </div>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
    <script src="//netdna.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
    <script>

      function update_trimesters(){
        var y = $('#sel_company').val();
        var url = '/year/' + y + '/list/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                $('#sel_trimester').empty().append('<optgroup label = "Choose a trimester">')
                for( var i = 0, len = result.length; i < len; i++ ) {
                    $('#sel_trimester').append('<option value="'+ result[i].id + '">'+ result[i].id + ' ' + result[i].name +'</option>')
                }
                $('#sel_trimester').append('</optgroup>');
                update_data();
            }
        });
      }

      function update_years(){
        var c = $('#sel_company').val();
        var url = '/company/' + c + '/list/';
        $.ajax({
            url: url,
            type: 'GET',
            traditional: true,
            dataType: 'json',
            success: function(result){
                $('#sel_year').empty().append('<optgroup label = "Choose a tax year">')
                for( var i = 0, len = result.length; i < len; i++ ) {
                    $('#sel_year').append('<option value="'+ result[i].id + '">'+ result[i].id + ' ' + result[i].name +'</option>')
                }
                $('#sel_year').append('</optgroup>');
                update_trimesters();
            }
        });
      }

      

      $('#sel_trimester').change(function() {
        update_data();
        
      });
      $('#sel_year').change(function() {
        update_trimisters();
        
      });
      $('#sel_company').change(function() {
        update_years();
      });
      
    </script>
    {% block js %}
    {% endblock %}
  </body>
</html>
