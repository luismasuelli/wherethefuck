"""
Points of interest are the stuff we search for. This means: we use some kind of polygon or circle
  distance, and we retrieve the points of interest that belong to that distance or that polygon.
"""


from functools import reduce
from django.db import models
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.db.models import PointField
from django.utils.translation import ugettext_lazy as _
from category.models import Category
from .base import SoftDeletedQueryset, Described


class POIQuerySet(SoftDeletedQueryset):

    def within(self, point, distance):
        """
        Returns all the POIs within a given radius.
        :param point: The center point.
        :param distance: The radius, in meters.
        :return: A new queryset for that condition.
        """

        return self.filter(location__distance_lte=(point, distance))

    def annotate_distances(self, **points):
        """
        Given all the keyword arguments, which MUST be points, annotates
          the queryset with distances for all those points, with respect
          to the POI locations.
        :return: A new queryset with all the distances being annotated
          given their keys AND their values (which are reference points).
        """

        return self.annotate(**{k: Distance('location', v) for k, v in points.items()})

    def nearby_search(self, point, distance, output_field='distance'):
        """
        Returns a queryset filtering by a required distance from a point, and also
          ordering by such distance.
        :param point: The reference point being the center of the search.
        :param distance: The radius, in meters.
        :param output_field: The output field name, which will be the field to hold
          the distance and order by it. The field must NOT exist. By default, 'distance'.
        :return: A new queryset, with the filter & sort criteria.
        """

        return self.within(point, distance).annotate_distances(**{output_field: point}).order_by(output_field)

    def in_region(self, regions):
        """
        Returns a queryset filtering all the points by one or more required regions (with certain geometry).
        Accepted/returned points will be the ones that belong to one or more of the specified regions. For
          an intersection criterion, several chained calls to this method will do the trick.
        :param regions: An iterable with regions to search by.
        :return: A new queryset for that condition.
        """

        return self.filter(reduce(lambda a, b: a | b, (models.Q(location__intersects=region.boundaries)
                                                       for region in regions if region.boundaries)))


class POI(Described):
    """
    POIs are the core of this system. They are literally points
      of interest, and will have name, image and description (Other
      fields MAY be added in the future or via plug-in).
    """

    # Image is optional for a POI, but adds some description.
    picture = models.ImageField(upload_to='pictures', blank=True, null=True, verbose_name=_('Picture'))
    # Filtering data (by category or location).
    location = PointField(verbose_name=_('Location'))
    categories = models.ManyToManyField(Category, blank=True, verbose_name=_('Categories'))

    objects = POIQuerySet.as_manager()

    class Meta:
        permissions = (
            ('manage_country_pois', 'Can manage POIs in specific countries'),
            ('manage_region_pois', 'Can manage POIs in specific regions'),
        )
        verbose_name = _('POI')
        verbose_name_plural = _('POIs')
