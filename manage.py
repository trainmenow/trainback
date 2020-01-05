import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from trainback import create_app, db

from trainback.trainmanager.user_account.models import Account


app = create_app(os.getenv('APP_CONFIG') or 'dev')

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run()


@manager.command
def test():
    """Runs the unit tests."""

    # Code for unittesting


if __name__ == '__main__':
    manager.run()