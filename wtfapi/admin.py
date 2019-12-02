from django.contrib import admin
from django.contrib.gis.db.models import PointField, MultiPolygonField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _
from .fields import GMapPointField, GmapMultiPolygonField
from .models import POI, User, Country, Province


class UserAdmin(BaseUserAdmin):

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email')


class POIAdmin(admin.ModelAdmin):

    formfield_overrides = {
        PointField: {"widget": GMapPointField}
    }


class RegionAdmin(admin.ModelAdmin):

    formfield_overrides = {
        MultiPolygonField: {"widget": GmapMultiPolygonField}
    }


admin.site.register(User, UserAdmin)
admin.site.register(POI, POIAdmin)
admin.site.register((Country, Province), RegionAdmin)
