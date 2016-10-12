
Coins
-----
This is a test Django project showcasing proper use of libs, code style, and project structure.

Installation
============
* Unpack the archive
* Create a database you will use. Note that sqlite3 doesn't support row locking which is used for preventing race conditions. Suggested database is postgresql.
* Set up the database in ```settings.py```. Default engine is postgresql and database name 'coins'.
* Create a virtualenv and check if it is activated.
* Run ```pip install -r requirements.txt``` to install all dependencies.
* Create a django superuser (```./manage.py createsuperuser```).
* Run ```./manage.py migrate``` to set the database to its initial state.

Documentation
=============
* Enter the ```docs``` directory and run ```make html``` to build the documentation. It will be accesible at ```./docs/_build/html/index.html```. 
* When the service is started, api documentation will be available at http://localhost:8000 (you have to be logged in to access it). You can log in with superuser credentials at http://localhost:8000/admin

Usage
=====
* Run tests with ```./manage.py test```.
* Start the service with ```./manage.py runserver```.
* Package ```httpie``` has been installed with project dependencies to ease testing. Check it out at https://github.com/jkbrzt/httpie and try using it for testing GET and POST requests.
* You can check PEP8 conformity by running ```flake8 .``` while in project dir.