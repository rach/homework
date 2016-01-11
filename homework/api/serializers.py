def serialize_listing(listing):
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": listing.coord},
        "properties": {
            "id": listing.id,
            "price": listing.price,
            "street": listing.street,
            "bedrooms": listing.bedrooms,
            "bathrooms": listing.bathrooms,
            "sq_ft": listing.sq_ft
        }
    }


def serialize_listing_list(request, listings):
    features = [serialize_listing(l) for l in listings]
    return {
        "type": "FeatureCollection",
        "features": features
    }
