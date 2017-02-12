The Pre-requisites for Development (Linux)
--------------------------------------

Asssuming you are using a Linux distribution that uses aptitude as its package
manager (e.g. Ubuntu, Debian, Mint), install the minimal required packages for
running the Django development server:

    sudo apt-get install mysql-server libmysqlclient-dev python-dev python-pip git

Once pip (the Python package installer) has been installed we need to install
the virtualenv tool.  Once installed, we can use pip and virtualenv to manage
all other Python package dependencies.

    sudo pip install virtualenv


Developing on OS X
------------------

If you are developing on a Mac you will have to downloand and install MySQL
manually.  You will also have to use easy_install to install/update pip:

    sudo easy_install pip

If you get Django errors along the lines of "Error loading MySQLdb module"
and/or "Library not loaded: libmysqlclient.18.dylib", try running the following
commands:

    sudo mkdir /usr/local/lib
    sudo ln -s /usr/local/mysql/lib/libmysqlclient.18.dylib /usr/local/lib/libmysqlclient.18.dylib


Checking out the Source Code
----------------------------

Changes to the DWAD project source code are tracked by the Git version control
system.  The master version of the project is stored on GitHub
(https://github.com/dwad/dwad.org), access to which is restricted to members of
the DWAD organisation on GitHub.  Assuming you have a GitHub account, have
uploaded your public SSH key and been granted access to the project, you can get
a copy of the project source code with the following command:

   git clone git@github.com:dwad/dwad.org.git dwad

This will clone the code into a directory called dwad under the current working
directory.  Where you store the code is not particularly important but the
directory must be called 'dwad' (all lowercase) otherwise Django will not work.
For development this directory will usually be somewhere under your home
directory.


Configuring the Python Virtual Environment
------------------------------------------

The virtualenv tool allows Python developers to isolate dependencies for
projects and to create multiple different environments that can be easily
switched between.

To create a virtualenv for the DWAD project, run the following commands (the
choice of directory locations is unimportant):

    mkdir ~/virtualenv
    virtualenv ~/virtualenv/dwad

You must activate a virtualenv to use it (your shell prompt will change to
indicate that you are currently using a virtualenv):

    . ~/virtualenv/dwad/bin/activate

Once activated, you can automatically install the project dependencies using
pip (these dependencies will only be available when the virtualenv is active):

    pip install -r ~/dwad/requirements.txt

NOTE: On Ubuntu you may have some problems installing Pillow, the Python 
Imaging Library.  It will install but without JPEG support, which is not at all 
useful.  So before running the pip install command above, make sure you install
the necessary libraries first:

    sudo apt-get install libfreetype6-dev libjpeg62 libjpeg62-dev libpng12-dev


Creating the DWAD Database
--------------------------

Login to the MySQL server using the command line client and the root username
and password:

    mysql -u root -p

Then create the DWAD database and a user to access it:

    CREATE DATABASE dwad CHARACTER SET utf8 COLLATE utf8_general_ci;
    GRANT ALL PRIVILEGES ON dwad.* TO 'dwad'@'localhost' IDENTIFIED BY '7LWo1SXqdJF69PL';

The username and password must be the same as those specified in the Django
settings.py file.  DO NOT USE THE MYSQL ROOT USER FOR DJANGO.


Importing Initial Data
----------------------

To create the database tables and import some initial data, including users and
Super 10 entries, run the following commands:

    ./manage.py syncdb --noinput
    ./manage.py createcachetable cache

Note that you will get errors if you try to run Django mangement commands
without first activating the virtualenv (see above).

As an alternative to installing the (probably out-dated) default data, you can
initialise your database from the latest MySQL dump from the live server.


Running the Development Server
------------------------------

By default the development server runs on port 8000 and only accepts connections
from the local machine:

    ./manage.py runserver

The site is then accessible at http://localhost:8000

To accept connections from other machines, bind to 0.0.0.0.  You may optionally
also change the port:

    ./manage.py runserver 0.0.0.0:3000

The site is then accessible at http://<your IP address>:3000


##### YOU CAN IGNORE THE REST OF THIS FILE IF YOU ARE NOT DEPLOYING TO THE LIVE SERVER #####

Pre-requisites for Deployment (Linux)
-------------------------------------

To run the site on a public-facing server, you can't use the Django development
server as that is massively insecure and not designed for high traffic levels.
Instead you need a web server to handle requests and pass them on to Django via
WSGI.  To use Apache as the web server you will need to install additional
packages:

    sudo apt-get install apache2 libapache2-mod-wsgi

Enable the required Apache modules:

    sudo a2enmod ssl
    sudo a2enmod wsgi
    sudo a2enmod rewrite
    sudo a2enmod expires


WSGI and SSL Configuration (Apache)
-----------------------------------

A copy of the current Apache virtual host configuration for dwad.org is in the
'apache' directory of the project.


Deploying Django Project Files
------------------------------

Do not use Git to checkout the project on the live server as this would require
storing your private SSH key on the server.  Instead, use rsync to copy files
from your local machine to the /usr/share/dwad directory on the web server.  The
script update.sh is provided to make this easier. Run the following command from
the dwad directory on your development machine:

    ./upload.sh <username>

The username you use should be a user at dwad.org who is a member of the
'dwadadmin' group, otherwise it will not have permission to write to
/usr/share/dwad.

If you have modified any static files (e.g. CSS, JavaScript or images), you
need to run the Django management command on the server to copy these files into
a location where they can be served by Apache:

    ./manage.py collectstatic


Crontab Configuration for Backups and Result Imports
----------------------------------------------------

Daily or hourly tasks can be configured in the crontab for a particular user.
To edit the crontab for the logged in user, run the following command:

    crontab -e

Currently on the dwad.org server, these crontab entries are configured for the
user 'dan'.  The first runs an import of results from football-data.co.uk at
midnight (server time, i.e. UTC, not BST) every day.  The second exports the
database and sends it to DropBox at 1am every day.

    0 0 * * *  cd /usr/share/dwad && . ../dwad-virtualenv/bin/activate && python manage.py importresults 1> /dev/null && deactivate
    0 1 * * *  cd /usr/share/dwad && . ../dwad-virtualenv/bin/activate && python manage.py dbbackup --compress 1> /dev/null && deactivate

