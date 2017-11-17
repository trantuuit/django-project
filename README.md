# Backend movie recommendation system
=============================================================================
### Create a virtualenv to isolate our package dependencies locally
- cd tutorial
- virtualenv -p python3 env
- source env/bin/activate  # On Windows use `env\Scripts\activate`

### Install packages into the virtualenv
- pip install django==1.11.7
- pip install djangorestframework==3.3.3
- pip install cassandra-driver==3.11.0
- pip install django-cassandra-engine==1.2.2
- pip install djangorestframework-jwt
- pip install Pygments==2.2.0

### Run project
- cd tutorial
- python manage.py runserver
