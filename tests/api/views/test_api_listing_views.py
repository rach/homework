import pytest
from homework.core.models import Listing, ListingStatus
from geoalchemy2.elements import WKTElement


@pytest.fixture
def listings(db_session):
    l1 = Listing(
        status=ListingStatus.active,
        price=10000,
        street="here",
        sq_ft=1000,
        bedrooms=2,
        bathrooms=1,
        coord=WKTElement("POINT(%0.10f %0.10f)" % (-110, 33), srid=4326)
    )
    db_session.add(l1)
    l2 = Listing(
        status=ListingStatus.active,
        price=20000,
        street="here",
        sq_ft=2000,
        bedrooms=4,
        bathrooms=2,
        coord=WKTElement("POINT(%0.10f %0.10f)" % (-113, 33), srid=4326)
    )
    db_session.add(l2)
    l3 = Listing(
        status=ListingStatus.active,
        price=30000,
        street="here",
        sq_ft=3000,
        bedrooms=5,
        bathrooms=4,
        coord=WKTElement("POINT(%0.10f %0.10f)" % (-110, 32), srid=4326)
    )
    db_session.add(l3)
    db_session.flush()
    l4 = Listing(
        status=ListingStatus.sold,
        price=40000,
        street="here",
        sq_ft=4000,
        bedrooms=6,
        bathrooms=5,
        coord=WKTElement("POINT(%0.10f %0.10f)" % (-110, 32), srid=4326)
    )
    db_session.add(l4)
    db_session.flush()

def test_filter_views(testapp, listings):

    response = testapp.get(
        '/listings',
    )
    assert response.status_code == 200
    assert len(response.json_body['features']) == 3


def test_filter_views_status(testapp, listings):

    response = testapp.get(
        '/listings',
        params={'status': 'sold'}
    )
    assert response.status_code == 200
    assert len(response.json_body['features']) == 1
    response = testapp.get(
        '/listings',
        params={'status': 'all'}
    )
    assert response.status_code == 200
    assert len(response.json_body['features']) == 4

def test_filter_views_with_price(testapp, listings):

    response = testapp.get(
        '/listings',
        params={'min_price': 20000}
    )
    assert response.status_code == 200
    assert len(response.json_body['features']) == 2
    response = testapp.get(
        '/listings',
        params={'min_price': 20000, 'max_price':20001}
    )
    assert response.status_code == 200
    assert len(response.json_body['features']) == 1

def test_filter_views_with_bedrooms(testapp, listings):

    response = testapp.get(
        '/listings',
        params={'min_bed': 3}
    )
    assert response.status_code == 200
    assert len(response.json_body['features']) == 2
    response = testapp.get(
        '/listings',
        params={'min_bed': 3, 'max_bed':4}
    )
    assert response.status_code == 200
    assert len(response.json_body['features']) == 1

def test_filter_views_with_bathrooms(testapp, listings):

    response = testapp.get(
        '/listings',
        params={'min_bath': 2}
    )
    assert response.status_code == 200
    assert len(response.json_body['features']) == 2
    response = testapp.get(
        '/listings',
        params={'min_bath': 2, 'max_bath':3}
    )
    assert response.status_code == 200
    assert len(response.json_body['features']) == 1

def test_filter_views_with_coords(testapp, listings):

    response = testapp.get(
        '/listings',
        params={'coord': "%s,%s" % (-113, 33), 'distance':1 }
    )
    assert response.status_code == 200
    assert len(response.json_body['features']) == 1
