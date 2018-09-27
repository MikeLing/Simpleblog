#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role, Post, Follow, Permission, Admin
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
import sys
if sys.version_info.major < 3:
    reload(sys)
sys.setdefaultencoding('utf8')

app = create_app(os.getenv('CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post,\
                Follow=Follow, Permission=Permission, Admin=Admin)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def deploy():
    from flask_migrate import upgrade
    from app.models import Role
    upgrade()
    Role.insert_roles()


if __name__ == '__main__':
    manager.run()
