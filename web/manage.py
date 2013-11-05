from flask.ext.script import Manager
import rethinkdb

from app import app


manager = Manager(app)


@manager.command
def db_setup():
    rethinkdb.connect(app.config['RETHINK_ADDRESS'], app.config['RETHINK_PORT']).repl()
    
    try:
        rethinkdb.db_create(app.config['RETHINK_DATABASE']).run()
        print 'DATABASE %s CREATED' % app.config['RETHINK_DATABASE']
    except rethinkdb.errors.RqlRuntimeError:
        print 'DATABASE ALREADY EXISTS'
        
    try:
        rethinkdb.db(app.config['RETHINK_DATABASE']).table_create('logs').run()
        print 'CREATED TABLE logs'
    except rethinkdb.errors.RqlRuntimeError:
        print 'TABLE logs ALREADY EXISTS'

    try:
        rethinkdb.db(app.config['RETHINK_DATABASE']).table_create('urls').run()
        print 'CREATED TABLE urls'
    except rethinkdb.errors.RqlRuntimeError:
        print 'TABLE urls ALREADY EXISTS'


@manager.command
def db_teardown():
    pass


@manager.command
def import_skybot_db():
    pass


if __name__ == '__main__':
    manager.run()
