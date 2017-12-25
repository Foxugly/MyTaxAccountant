
import os

db = {  'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(os.path.dirname(__file__), 'db.sqlite3'),
        }
#        'default': {
#            'ENGINE': 'django.db.backends.mysql', # 'django.db.backends.postgresql_psycopg2' for postgresql
#            'NAME': 'DB_NAME',
#            'USER': 'DB_USER',
#            'PASSWORD': 'DB_PASSWORD',
#            'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
#            'PORT': '3306',
#        }
    }

