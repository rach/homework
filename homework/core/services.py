from homework.core.models import Listing, ListingStatus
from sqlalchemy.exc import IntegrityError
from geoalchemy2.elements import WKTElement
from geoalchemy2.functions import ST_Distance


class ListingService(object):

    def __init__(self, dbsession):
        self.dbsession = dbsession

    def create_listing(self, status, street, price, bedrooms, bathrooms, sq_ft,
                       lat, lng, pid=None):
        """
        This code has rollback and savepoint to support concurrent insert with
        unique constraint primary id as we allow to set it.
        """
        created = False
        if pid is not None:  # not None because the first imported id == 0
            listing = self.get_listing_by_id(pid)
            if listing:
                return listing, created

        position = "POINT(%0.10f %0.10f)" % (lng, lat)
        listing = Listing(
            status=ListingStatus.from_string(status),
            price=price,
            street=street,
            sq_ft=sq_ft,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            coord=WKTElement(position, srid=4326)
        )
        if pid is not None:
            listing.id = pid
        self.dbsession.begin_nested()
        try:
            self.dbsession.add(listing)
            self.dbsession.commit()
            created = True
        except IntegrityError:
            self.dbsession.rollback()
            listing = self.get_listing_by_id(pid)

        return listing, created

    def get_listing_by_id(self, id):
        return self.dbsession.query(Listing).filter(Listing.id == id).first()

    def filter_listings(self, status=None,
                        min_price=None, max_price=None,
                        min_bed=None, max_bed=None,
                        min_bath=None, max_bath=None,
                        distance=None, coord=None, after=None, before=None):

        size = 10
        query = self.dbsession.query(Listing)
        is_before = is_after = False
        reorder_fct = lambda x: x
        order = Listing.id
        if status != 'all':
            status = status or 'active'
            query = query.filter(Listing.status == ListingStatus.from_string(status))
        if min_price is not None:
            query = query.filter(Listing.price >= min_price)
        if max_price is not None:
            query = query.filter(Listing.price <= max_price)
        if min_bath is not None:
            query = query.filter(Listing.bathrooms >= min_bath)
        if max_bath is not None:
            query = query.filter(Listing.bathrooms <= max_bath)
        if min_bed is not None:
            query = query.filter(Listing.bedrooms >= min_bed)
        if max_bed is not None:
            query = query.filter(Listing.bedrooms <= max_bed)

        if coord and distance:
            # POSTGIS is lon, lat and not lat, lon
            pt = WKTElement('POINT({0} {1})'.format(*coord), srid=4326)
            query = query.filter(ST_Distance(Listing.coord, pt, True) <= (distance * 1000))

        # Pagination without offset to optimize index usage, key set pagination

        if before is None and after is None:
            if query.limit(size + 1).count() > size:
                is_after = True

        if after is not None:
            query = query.filter(Listing.id > after)
            is_before = True
            if query.order_by(Listing.id).limit(size + 1).count() > size:
                is_after = True

        if before is not None:
            is_after = True
            order = Listing.id.desc()
            reorder_fct = lambda x: list(reversed(x))
            query = query.filter(Listing.id < before)
            if query.order_by(Listing.id.desc()).limit(size + 1).count() > size:
                is_before = True

        # End pagination

        listings = query.order_by(order).limit(size).all()
        return reorder_fct(listings), is_before, is_after
