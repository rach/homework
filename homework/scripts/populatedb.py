import os
import sys
from cStringIO import StringIO
import requests
import csv
from sqlalchemy import create_engine
from schematics.exceptions import ModelValidationError, ModelConversionError
from homework.core.schemas import ListingImportSchema
from homework.core.services import ListingService

from pyramid.paster import (
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

def csv_row_to_schema(row):
    val = {
        'pid': row[0],
        'street': row[1],
        'status': row[2],
        'price': row[3],
        'bedrooms': row[4],
        'bathrooms': row[5],
        'sq_ft': row[6],
        'coord': (float(row[7]), float(row[8]))
    }
    return ListingImportSchema(val)

def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    engine = create_engine('postgresql://homework@/homework')
    dbsession  = create_dbsession(engine)
    service = ListingService(dbsession)
    r = requests.get('https://s3.amazonaws.com/opendoor-problems/listings.csv')
    if not r.ok:
        exit(1)
    failed, imported = [], 0;
    reader = csv.reader(StringIO(r.text))
    reader.next()  # Skip header
    for row in reader:
        schema = csv_row_to_schema(row)
        try:
            schema.validate()
            service.create_listing(
                pid=schema.pid,
                street=schema.street,
                status=schema.status,
                price=schema.price,
                sq_ft=schema.sq_ft,
                bedrooms=schema.bedrooms,
                bathrooms=schema.bathrooms,
                lat=schema.coord[0],
                lng=schema.coord[1],
            )
            imported += 1
        except (ModelConversionError, ModelValidationError), e:
            print e.messages
            failed.append(row[0])
    dbsession.commit()
    print 'Successfully imported: %s' % imported
    print 'Failed: %s' % len(failed)
    print 'Failed ids: %s' % failed
