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
    <link rel="stylesheet" href="{% static "viewer/viewer.min.css"%}">
    {% block css %}
    {% endblock %}
    <link href='{% static "css/perso.css" %}' rel='stylesheet' />
    <!--  JS -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
    <script src='{% static "viewer/viewer.min.js" %}'></script>
    <!--<script src='{% static "viewer/main.js" %}'></script>-->
    {% block js %}
    {% endblock %}
    {% block header %}
    {% endblock %}
  </head>
  <body>
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
        <div class="docs-galley">
		<ul class="docs-pictures clearfix">
			<li><img data-original="https://raw.githubusercontent.com/fengyuanchen/viewerjs/master/assets/img/tibet-1.jpg" src="https://raw.githubusercontent.com/fengyuanchen/viewerjs/master/assets/img/thumbnails/tibet-1.jpg" alt="Picture1"></li>
                        <li><img data-original="https://raw.githubusercontent.com/fengyuanchen/viewerjs/master/assets/img/tibet-2.jpg" src="https://raw.githubusercontent.com/fengyuanchen/viewerjs/master/assets/img/thumbnails/tibet-2.jpg" alt="Picture2"></li>
		</ul>
	</div>
      </div>
    </div>
    <script>
       window.onload = function () {
  'use strict';
        var Viewer = window.Viewer;
        var pictures = document.querySelector('.docs-pictures');
        var viewer;
        viewer = new Viewer(pictures);
};
    </script>
 </body>
</html>
