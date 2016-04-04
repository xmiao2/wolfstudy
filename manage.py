import os
from wolfstudy import create_app, db
from flask.ext.script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand

app     = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
host    = '0.0.0.0'
port    = '5000'

manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(
    use_debugger = True,
    use_reloader = True,
    host = host,
    port = port) )

if __name__ == '__main__':
    manager.run()
