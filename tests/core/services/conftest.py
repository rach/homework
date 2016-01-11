from homework.core.services import ListingService
import pytest


@pytest.fixture
def listing_svc(db_session):
    return ListingService(db_session)
