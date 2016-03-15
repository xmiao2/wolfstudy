WolfStudy
=========

This is the Git repository for WolfStudy, an open question and answer site for students.

Running the development server
------------------------------

0. Create the `virtualenv`: `$ virtualenv venv`.
1. Activate the `virtualenv`: `$ . venv/bin/activate`.
2. Install the requirements: `$ venv/bin/pip install -r requirements.txt`.
3. Edit code.
4. Run the application: `$ python2 manage.py runserver`.
5. When you're done working, run `$ deactivate`.

Deploying to Heroku
-------------------

Run `$ git push heroku master` to deploy from master.

Run `$ git push heroku <yourbranch>:master` to deploy from a different branch called `<yourbranch>`.
