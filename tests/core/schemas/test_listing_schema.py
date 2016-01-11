from homework.core.schemas import ListingImportSchema
from schematics.exceptions import ModelValidationError, ModelConversionError
import pytest


def test_valid_link_schema():
    schema = ListingImportSchema({
        "pid": 0,
        "status": "active",
        "price": 10000,
        "sq_ft": 1000,
        "bathrooms": 2,
        "bedrooms": 3,
        "street": "here",
        "coord": (-112.1151215344, 33.4767593059)
    })
    schema.validate()


def test_listing_schema_all_required():
    schema = ListingImportSchema({})
    with pytest.raises(ModelValidationError) as excinfo:
        schema.validate()
    assert set(['pid',
                'status',
                'price',
                'sq_ft',
                'bathrooms',
                'bedrooms',
                'street',
                'coord']) == set(excinfo.value.messages.keys())




def test_link_schema_with_invalid_numbers():
    schema = ListingImportSchema({
        "pid": 0,
        "status": "active",
        "price": 0,
        "sq_ft": 0,
        "bathrooms": 0,
        "bedrooms": 0,
        "street": "here",
        "coord": (-112.1151215344, 33.4767593059)
    })
    with pytest.raises(ModelValidationError) as excinfo:
        schema.validate()
    assert set(['price',
                'sq_ft',
                'bathrooms',
                'bedrooms']) == set(excinfo.value.messages.keys())


@pytest.mark.skipif(True, reason="Schematics doesn't yet validate the min/max of lon/lat")
def test_link_schema_with_invalid_coords():
    schema = ListingImportSchema({
        "pid": 0,
        "status": "active",
        "price": 10000,
        "sq_ft": 1000,
        "bathrooms": 1,
        "bedrooms": 2,
        "street": "here",
        "coord": (-181.1151215344, 91.4767593059)
    })
    with pytest.raises(ModelValidationError) as excinfo:
        schema.validate()
    assert 'coord' in str(excinfo.value)
