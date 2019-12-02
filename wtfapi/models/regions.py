"""
Points of interest are the stuff we search for. This means: we use some kind of polygon or circle
  distance, and we retrieve the points of interest that belong to that distance or that polygon.
"""


from django.db import models
from django.contrib.gis.db.models import MultiPolygonField
from django.utils.translation import ugettext_lazy as _
from .base import SoftDeletedQueryset, Described


class Region(Described):
    """
    Regions are geographical boundaries which will come in 2 different levels:
    - Country
    - Province
    They will only know their boundaries data. They will also be MANAGED by certain
      staff members that can be assigned to them. Remarks in particular for each
      region.
    """

    # Filtering data (by region).
    boundaries = MultiPolygonField(verbose_name=_('Boundaries'))
    # Managers.
    managers = models.ForeignKey('User', related_name='managed_%(class)s_records', blank=True, on_delete=models.PROTECT)

    class Meta:
        abstract = True


class CountryQuerySet(SoftDeletedQueryset):
    """
    Country query sets allow us to get the list of country-related records (e.g. POIs, regions) that can be
      managed by certain user (provided they have also the permission to manage them at admin level).
    """

    def allowed_for(self, user):
        if user.is_superuser:
            return self
        else:
            return self.filter(managers=user)


class Country(Region):
    """
    Countries will be the top-level regions, and will have country-level managers.
    """

    objects = CountryQuerySet.as_manager()

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')


class ProvinceQuerySet(SoftDeletedQueryset):
    """
    Province query sets allow us to get the list of province-related records (e.g. POIs) that can be
      managed by certain user (provided they have also the permission to manage them at admin level).
    """

    def allowed_for(self, user):
        return self.filter(models.Q(managers=user) | models.Q(country__in=Country.objects.allowed_for(user)))


class Province(Region):
    """
    Provinces will be just below the countries, and will have province-level managers.
    Provinces themselves will be editable by country-level managers, but the data linked
      to the province(s) will be editable by both country-level managers and province-level
      managers.
    """

    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="provinces")
    objects = CountryQuerySet.as_manager()

    class Meta:
        verbose_name = _('Province')
        verbose_name_plural = _('Provinces')
