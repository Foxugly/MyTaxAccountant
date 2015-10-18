# MyTaxAccoutant
**MyTaxAccountant** is a open source website that give the opportunity of smalls companys of independant to upload their tax documents (sales, invoice,...).<br>
Each user can have 0-n companies.<br>
Each company can have 0-n tax years.<br>
Each tax year can have 0-n trimesters.<br>
Each trimester can have 0-n documents.<br>
<br>
We can upload image files and pdf files. For pdfs, the idea is to run a thread to convert pdfs in a set of png.<br>
<br>
Using Django 1.8, bootstrap 3, datatables, jquery and ajax

Installation
============

To install:
    pip install -r requirements.txt
    python manage.py syncdb
    python manage.py migrate

To add a test set:
    python manage.py shell < data.py
