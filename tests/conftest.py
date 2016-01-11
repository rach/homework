import pytest
from sqlalchemy import create_engine
from homework.core.models.meta import create_dbsession, Base
import zope.sqlalchemy
from pyramid import testing
from pyramid_services import find_service
from zope.interface.adapter import AdapterRegistry
from webtest import TestApp
import types
import os


@pytest.fixture(scope='session')
def db(request):
    """Session-scoped sqlalchemy database connection"""
    engine = create_engine('postgresql://homework@/homework_test')
    dbsession = create_dbsession(engine)
    dbsession.execute('CREATE EXTENSION IF NOT EXISTS postgis;')
    dbsession.execute('CREATE EXTENSION IF NOT EXISTS postgis_topology;')
    dbsession.commit()
    zope.sqlalchemy.register(dbsession)
    # we drop before to be sure we didn't leave the previous state unclean
    Base.metadata.drop_all()
    Base.metadata.create_all()
    dbsession.registry.clear()
    request.addfinalizer(Base.metadata.drop_all)
    return dbsession


@pytest.fixture
def db_session(request, db):
    """Function-scoped sqlalchemy database session"""
    from transaction import abort
    trans = db.connection().begin()
    request.addfinalizer(trans.rollback)
    request.addfinalizer(abort)
    return db



@pytest.fixture
def config(request):
    config = testing.setUp()
    config.include('pyramid_services')
    request.addfinalizer(testing.tearDown)
    return config

@pytest.fixture
def dummy_request(request, config):
    req = testing.DummyRequest()
    req.find_service = types.MethodType(find_service, req)
    req.service_cache = AdapterRegistry()
    return req


@pytest.fixture
def testapp(db_session):
    from homework.api import main
    os.environ['DATABASE_URL'] = 'postgresql://homework@/homework_test'
    return TestApp(main({'dbsession': db_session}))
