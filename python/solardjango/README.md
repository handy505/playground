# Virtual Enviroment
$ python3 -m venv VENV
$ sudo apt-get install python3-venv


# Entry/Exit Virtual Enviroment
$ source VENV/bin/activate
(VENV) ... $ deactivate

# Install pip3 on Ubuntu
$ sudo apt install python3-pip

# Database operate
$ sudo apt install sqlite3
$ sudo apt install sqlitebrowser

# Backup/Sync Virtual Enviroment
$ pip freeze > requirments.txt
$ pip install -r requirements.txt

# Install Django
$ pip install --upgrade pip
$ pip install django
$ pip list

# Start Django project
$ django-adminn.py startproject locallibrary

# Add feature
$ python3 manage.y startapp blog

# Run server
$ python3 manage.py runserver

# Sync Database(After Django2)
$ python3 manage.py makemigrations
$ python3 manage.py migrate

# Operate Database Manually 
$ python manage.py createsuperuser


