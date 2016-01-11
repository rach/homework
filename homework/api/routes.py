

def includeme(config):
    config.add_route('listings', '/listings*traverse',
                     factory='homework.api.resources.ListingFactory')
