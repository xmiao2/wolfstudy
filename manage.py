import os
from wolfstudy import create_app, db
from wolfstudy.models import Question, Answer, User
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, Question=Question, Answer=Answer, User=User)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def deploy():
    from flask.ext.migrate import upgrade
    upgrade()

if __name__ == '__main__':
    manager.run()
