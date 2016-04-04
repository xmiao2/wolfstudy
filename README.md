WolfStudy
=========

This is the Git repository for WolfStudy, an open question and answer site for students.

Running the development server
------------------------------

0. Create the `virtualenv`: `$ virtualenv venv`.
1. Activate the `virtualenv`: `$ . venv/bin/activate`.
2. Install the requirements: `$ venv/bin/pip install -r requirements.txt`.
3. Edit code.
4. Run the application: `$ python2 manage.py runserver`. (Change the IP and Port in manage.py if needed.)
5. When you're done working, run `$ deactivate` or CTRL+C.

Common Problem
--------------

- On first run, if you see 500 errors stating that tables cannot be found. Run `$ python2 manage.py db downgrade` then `$ python2 manage.py db upgrade` (This will no longer be necessary once db is migrated to PostgreSQL).

Deploying to Heroku
-------------------

Run `$ git push heroku master` to deploy from master.

Run `$ git push heroku <yourbranch>:master` to deploy from a different branch called `<yourbranch>`.
