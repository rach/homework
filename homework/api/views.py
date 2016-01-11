from pyramid.view import view_config, view_defaults
from homework.api.forms import ListingFilterForm
from homework.api.resources import ListingResource
from homework.api import serializers
from pyramid.httpexceptions import HTTPBadRequest
import json

from pyramid.view import (
    notfound_view_config
)


@notfound_view_config(renderer='json')
def notfound(request):
    request.response.status = 404
    return {}

@view_defaults(route_name='listings', renderer='json')
class ListingView():

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.listing = context.unwrap()
        self.response = request.response
        self.listing_svc = request.find_service(name='listing')

    @view_config(request_method='OPTIONS')
    @view_config(context=ListingResource, request_method='OPTIONS')
    def options_request(self):
        self.response.headers['ALLOW'] = 'GET'

    def header_links(self, listings, is_before, is_after):
        params = self.request.params.copy()
        params.pop('after', None)
        params.pop('before', None)
        header_links = []
        if is_before or is_after:
            header_links.append(
                '<%s>; rel="first"' % self.request.current_route_url(_query=params)
            )
        if is_before:
            params['before'] = listings[0].id
            header_links.append(
                '<%s>; rel="prev"' % self.request.current_route_url(_query=params)
            )
            del params['before']

        if is_after:
            params['after'] = listings[-1].id
            header_links.append(
                '<%s>; rel="next"' % self.request.current_route_url(_query=params)
            )
            del params['after']

        if header_links:
            self.response.headers['LINKS'] = ', '.join(header_links)

    @view_config(request_method='GET')
    def filter_listings(self):
        form = ListingFilterForm(self.request.params)
        if form.validate():

            listings, is_before, is_after = self.listing_svc.filter_listings(
                status=form.data['status'],
                min_price=form.data['min_price'],
                max_price=form.data['max_price'],
                min_bed=form.data['min_bed'],
                max_bed=form.data['max_bed'],
                min_bath=form.data['min_bath'],
                max_bath=form.data['max_bath'],
                distance=form.data['distance'],
                coord=form.data['coord'],
                after=form.data['after'],
                before=form.data['before']
            )
            self.header_links(listings, is_before, is_after)
            return serializers.serialize_listing_list(self.request, listings)
        return HTTPBadRequest(json.dumps({'errors': form.errors}))

    @view_config(context=ListingResource, request_method='GET')
    def get_listing(self):
        return serializers.serialize_listing(self.context.unwrap())
