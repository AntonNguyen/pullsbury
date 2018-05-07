from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, exc
from sqlalchemy.pool import Pool
import contextlib
import logging


db = SQLAlchemy()
log = logging.getLogger(__name__)


@contextlib.contextmanager
def transactional():
    try:
        yield
        db.session.commit()
    except:
        db.session.rollback()


def truncate_all_tables():
    db.engine.execute('SET FOREIGN_KEY_CHECKS = 0;')
    for table in db.metadata.sorted_tables:
        db.engine.execute('TRUNCATE %s;' % table.name)
    db.engine.execute('SET FOREIGN_KEY_CHECKS = 1;')


db.truncate_all_tables = truncate_all_tables


@event.listens_for(Pool, "connect")
def on_connect(dbapi_connection, connection_record):
    log.info('Setting timezone to UTC')
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("SET SESSION time_zone = '+0:00'")
        cursor.close()
    except Exception as error:
        log.exception(error)


@event.listens_for(Pool, 'checkout')
def ping_connection(dbapi_connection, connection_record, connection_proxy):
    """
    Because sometimes it may be hours without a request
    we need to gracefully handle MySQL killing our connections.
    While the pool_recycle catches most of this, it misses an annoying case
    where the we get 0 requests for longer than the pool_recycle + timeout
    length.
    """
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("SET SESSION time_zone = '+0:00'")
        cursor.close()
    except:
        log.info('Connection in pool has timed out and will be reconnected.')
        # The connection died before it was recycled.
        # Raise an exception force a reconnection.
        raise exc.DisconnectionError()


def save(instance):
    db.session.add(instance)
    db.session.flush()
    return instance


def commit_request_transaction(response):
    if response.status_code >= 200 and response.status_code < 400:
        try:
            db.session.commit()
        except:
            raise Exception()
    else:
        db.session.rollback()
    return response


db.Model.save = save
