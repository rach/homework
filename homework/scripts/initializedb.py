import os
import sys

from sqlalchemy import create_engine

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from homework.core.models.meta import (
    Base,
    create_dbsession
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    engine = create_engine(
        os.environ.get('DATABASE_URL',
                       'postgresql://homework@/homework')
    )
    dbsession = create_dbsession(engine)
    dbsession.execute('CREATE EXTENSION IF NOT EXISTS postgis;')
    dbsession.execute('CREATE EXTENSION IF NOT EXISTS postgis_topology;')
    dbsession.commit()
    Base.metadata.create_all(engine)
