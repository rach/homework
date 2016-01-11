class ResourceWrapper(dict):
    def __init__(self, resource):
        self.resource = resource

    def unwrap(self):
        return self.resource


class ListingFactory(object):

    def __init__(self, request):
        self.request = request

    def __getitem__(self, key):
        svc = self.request.find_service(name='listing')
        listing = svc.get_listing_by_id(key)
        if listing:
            return ListingResource(listing)
        raise KeyError(key)

    def unwrap(self):
        return None


class ListingResource(ResourceWrapper):
    __name__ = 'ListingResource'
    __parent__ = ListingFactory

    def __getitem__(self, key):
        raise KeyError(key)
