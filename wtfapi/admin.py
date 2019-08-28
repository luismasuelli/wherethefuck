from django.contrib import admin
from mapwidgets.widgets import GooglePointFieldWidget
from .models import POI, PointField


class POIAdmin(admin.ModelAdmin):
    formfield_overrides = {
        PointField: {"widget": GooglePointFieldWidget}
    }


admin.site.register(POI, POIAdmin)