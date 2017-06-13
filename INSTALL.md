WCIVF requires Python 3.

To install on Ubuntu 14.0.x (masochistically):

    sudo apt-get install python3-dev libpq-dev libjpeg-dev redis-server
    sudo apt-get install ruby
    sudo gem install --no-ri --no-rdoc sass -v 3.4.21
    sudo apt-get install python3-ipdb python3-pip
    pip3 install -r requirements/local.txt

Create a Postgres database as detailed below, then:

    ./manage.py migrate
    ./manage.py import_elections
    ./manage.py import_posts
    ./manage.py import_parties
    ./manage.py import_people

If you don't want to install Redis for some reason (like e.g. laziness) you can override
the cache backend with a file at `./wcivf/settings/local.py` with the following:

    CACHES = {
        'default': {
           'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

## Setting up PostgreSQL and PostGIS

By default WhoCanIVoteFor uses PostgreSQL with the PostGIS extension. To set this up locally, first install the packages:

    sudo apt-get install postgresql postgis

Then create, for example, a `wcivf` user:

    sudo -u postgres createuser -P wcivf

Set the password to, for example, `wcivf`. Then create the database, owned by the `wcivf` user:

    sudo -u postgres createdb -O wcivf wcivf

Finally, add the PostGIS extension to the database:

    sudo apt-get install postgresql-9.3-postgis-scripts #*
    sudo -u postgres psql -d wcivf -c "CREATE EXTENSION postgis;"

(* via [Stack Overflow](https://stackoverflow.com/questions/34134207/postgres-9-3-10-usr-share-postgresql-9-3-extension-postgis-control))

Then, create a file `wcivf/settings/local.py` with the following contents, assuming you used the same username, password and database name as above:

    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'wcivf',
            'USER': 'wcivf',
            'PASSWORD': '*****',
            'HOST': 'localhost',
            'PORT': '',
        }
    }


## Creating inline CSS

To regenerate the static files, `npm install -g yuglify`, then:

    manage.py collectstatic

The CSS for this project is inlined in the base template for performance reasons.

This is created using [`critical`](https://github.com/addyosmani/critical), and can be re-created by running

```
curl localhost:8000 | critical --base wcivf -m > wcivf/templates/_compressed_css.html
```
