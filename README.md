# MyTaxAccoutant
**MyTaxAccountant** is a open source website that give the opportunity of smalls companys of independant to upload their tax documents (sales, invoice,...).<br>
Each user can have 0-n companies.<br>
Each company can have 0-n tax years.<br>
Each tax year can have 0-n trimesters.<br>
Each trimester can have 0-n documents.<br>
<br>
We can upload image files and pdf files. For pdfs, the idea is to run a thread to convert pdfs in a set of png.<br>
<br>
Using Pyhon3, Django 2.0.2, bootstrap 3, datatables, jquery and ajax, celery, redis

Installation
============

To install:

        sudo apt-get update
	sudo apt-get upgrade
	sudo apt-get install -y python3-dev python3-setuptools python-celery-common libjpeg-dev zlib1g-dev libtiff5-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk imagemagick redis-server
	sudo pip install --upgrade pip
	sudo pip install -r requirements.txt
	python3 manage.py makemigrations
	python3 manage.py migrate
	python3 manage.py createsuperuser

To add a test set:

	python manage.py shell < data.py

To run on dev:

	python3 manage.py runserver
	service redis-server start
	redis-cli ping
	service apache2 restart
	su - www-data
	cd /var/www/MyTaxAccountant/
	celery -A mta worker -l info >> /tmp/celery.log &
	python3 manage.py shell_plus --notebook &
	
To run on docker

	docker run -p 443:443 -p 8888:8888 -p 6379:6379 -it --privileged mydocker /bin/bash
	mount -a
	service redis-server start
	redis-cli ping
	service apache2 restart
	su - www-data
	cd /var/www/MyTaxAccountant/
	celery -A mta worker -l info >> /tmp/celery.log &
	python3 manage.py shell_plus --notebook &

Translation
===========

to generate .po files : 

	django-admin.py makemessages -l=en
	django-admin.py makemessages -l=fr
	django-admin.py makemessages -l=nl

for english, french and dutch.

complete translations and compile :

	django-admin compilemessages --locale=en
	django-admin compilemessages --locale=fr
	django-admin compilemessages --locale=nl


