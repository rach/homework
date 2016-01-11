from homework.core.services import (
    ListingService
)
from sqlalchemy import create_engine
from homework.core.models.meta import (
    create_dbsession
)
import zope.sqlalchemy
import os


def includeme(config):
    engine = create_engine('postgresql://homework@/homework')
    if 'dbsession' not in config.registry.settings:
        dbsession = create_dbsession(engine)
        zope.sqlalchemy.register(dbsession)
    else:
        dbsession = config.registry.settings['dbsession']

    config.register_service(
        dbsession,
        name='db'
    )

    config.register_service(
        ListingService(dbsession),
        name='listing'
    )
