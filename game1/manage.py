# copypasta from https://flask-migrate.readthedocs.io/en/latest/
# used to shortcut management of database
#
# python manage.py db init
# python manage.py db migrate
# python manage.py db upgrade
# python manage.py db --help

import sys
import os
from game1 import app, db, db_dir
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    # move the migrations folder into same dir as db to keep things neat
    sys.argv.append("--directory")
    sys.argv.append(os.path.join(db_dir, "migrations"))
    manager.run()