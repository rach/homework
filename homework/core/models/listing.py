from sqlalchemy import (
    Column,
    Unicode,
    Integer,
    String,
    Index,
    CheckConstraint
)

from homework.core.models.meta import (
    Base,
    DeclEnum,
    TimestampColumns
)
from geoalchemy2 import Geometry


class ListingStatus(DeclEnum):
    active = "active", "Active"
    pending = "pending", "Pending"
    sold = "sold", "Sold"


class Listing(Base, TimestampColumns):
    status = Column(ListingStatus.db_type(), index=True)
    price = Column(Integer, CheckConstraint('price>=1'), nullable=False, )
    street = Column(String, nullable=False)
    bedrooms = Column(Integer, CheckConstraint('bedrooms>=1'), nullable=False)
    bathrooms = Column(Integer, CheckConstraint('bathrooms>=1'), nullable=False)
    sq_ft = Column(Integer, CheckConstraint('sq_ft>=1'), nullable=False)
    coord = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    __table_args__ = (
        Index('idx_status_price', status, price),
        Index('idx_status_bedrooms', status, bedrooms),
        Index('idx_status_bathrooms', status, bathrooms),
        Index('idx_status_price_bathrooms', status, price, bathrooms),
        Index('idx_status_price_bedrooms', status, price, bedrooms),
        Index('idx_status_price_', status, price, bedrooms),
    )
