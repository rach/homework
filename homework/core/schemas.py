from schematics.models import Model
from schematics.types import GeoPointType, IntType, StringType


class ListingImportSchema(Model):
    pid = IntType(required=True)
    status = StringType(choices=['active', 'pending', 'sold'], required=True)
    price = IntType(min_value=1, required=True)
    sq_ft = IntType(min_value=1, required=True)
    bathrooms = IntType(min_value=1, required=True)
    bedrooms = IntType(min_value=1, required=True)
    street = StringType(required=True)
    coord = GeoPointType(required=True)
