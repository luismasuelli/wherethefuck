from django.conf import settings
from floppyforms.gis import BaseGMapWidget, PointField, MultiPolygonField


class GMapPointField(PointField, BaseGMapWidget):
    google_maps_api_key = settings.GOOGLE_MAPS_API_KEY


class GmapMultiPolygonField(MultiPolygonField, BaseGMapWidget):
    google_maps_api_key = settings.GOOGLE_MAPS_API_KEY
    is_polygon = True
    is_collection = True
