from homework.core.models import Listing, ListingStatus
from geoalchemy2.elements import WKTElement
from sqlalchemy.exc import IntegrityError
import pytest


def test_create_listing(db_session):
    listing = Listing(
        status=ListingStatus.active,
        price=10000,
        street="here",
        sq_ft=1000,
        bedrooms=2,
        bathrooms=2,
        coord=WKTElement("POINT(%0.10f %0.10f)" % (-112, 33), srid=4326)
    )
    db_session.add(listing)
    db_session.flush()
    assert db_session.query(Listing).count() == 1


def test_create_link_constraintes(db_session):
    listing = Listing(
        status=ListingStatus.active,
        price=0,
        street="here",
        sq_ft=0,
        bedrooms=0,
        bathrooms=0,
        coord=WKTElement("POINT(%0.10f %0.10f)" % (-112, 33), srid=4326)
    )
    db_session.add(listing)
    with pytest.raises(IntegrityError) as excinfo:
        db_session.flush()
    db_session.rollback()
    assert db_session.query(Listing).count() == 0
