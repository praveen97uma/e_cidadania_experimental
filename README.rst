e-cidadania
===========

e-cidadania is a project to develop an open source application for citizen participation, usable by associations, companies and administrations.

The e-cidadania objective is to maintain the platform as easy as possible while improving in the user interface to be easier to use as possible.

Installation
------------

To install e-cidadania follow these steps:

* Download the source code from git, or from the official webpage.
* Go to src/
* python bootstrap.py
* bin/buildout
* Configure setting.py to you desire.

Now you must be in src/e_cidadania/

* Generate the database with::

    ../python2.7 manage.py syncdb

* Copy all the static files::

    ../python manage.py collectstatic

* Run the development server

    ../python manage.py runserver


