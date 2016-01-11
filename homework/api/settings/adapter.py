from pyramid.renderers import JSON
import datetime
from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape
from homework.core.models.meta import EnumSymbol

def enum_adapter(obj, request):
    return obj.value


def datetime_adapter(obj, request):
    return obj.isoformat()


def wkb_adapter(obj, request):
    shape = to_shape(obj)
    if shape.type == 'Point':
        return shape.coords[0]
    else:
        return shape.to_wkt()


def includeme(config):
    json_renderer = JSON()
    json_renderer.add_adapter(datetime.datetime, datetime_adapter)
    json_renderer.add_adapter(EnumSymbol, enum_adapter)
    json_renderer.add_adapter(WKBElement, wkb_adapter)
    config.add_renderer('json', json_renderer)
