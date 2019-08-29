from django.contrib import admin
from django.contrib.gis.db.models import PointField
from mapwidgets.widgets import GooglePointFieldWidget
from .models import POI


class POIAdmin(admin.ModelAdmin):
    formfield_overrides = {
        PointField: {"widget": GooglePointFieldWidget}
    }


admin.site.register(POI, POIAdmin)