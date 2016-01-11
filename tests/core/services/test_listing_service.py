from homework.core.models import Listing


def test_create_listing(db_session, listing_svc):
    _, created = listing_svc.create_listing(
        pid=101,
        street="here",
        status="active",
        price=10000,
        sq_ft=1000,
        bedrooms=2,
        bathrooms=1,
        lat=33,
        lng=-112,
    )
    assert created
    assert db_session.query(Listing).count() == 1


def test_create_listing_with_id(db_session, listing_svc):
    _, created = listing_svc.create_listing(
        pid=101,
        street="here",
        status="active",
        price=10000,
        sq_ft=1000,
        bedrooms=2,
        bathrooms=1,
        lat=33,
        lng=-112,
    )

    assert created
    assert db_session.query(Listing).count() == 1


def test_get_link_by_id(db_session, listing_svc):
    l1, created = listing_svc.create_listing(
        pid=101,
        street="here",
        status="active",
        price=10000,
        sq_ft=1000,
        bedrooms=2,
        bathrooms=1,
        lat=33,
        lng=-112,
    )
    assert created
    l2 = listing_svc.get_listing_by_id(l1.id)
    assert l2 is not None
    assert l1 == l2
