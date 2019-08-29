from django.contrib.gis.db.models.functions import Distance
from django.db import models
from django.contrib.gis.db.models import PointField
from django.utils.translation import ugettext_lazy as _
from category.models import Category


class POIQuerySet(models.QuerySet):

    def all(self):
        """
        Excludes the marked-as-deleted POIs.
        :return: A base queryset, excluding the deleted ones.
        """

        # If at least one of the two fields is null, it will count
        #   as deleted and not included in the regular queryset.
        return self.filter(deleted=False, deleted_by__isnull=True)

    def within(self, point, distance):
        """
        Returns all the POIs within a given radius.
        :param point: The center point.
        :param distance: The radius, in meters.
        :return: A queryset for that condition.
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


class POI(models.Model):
    """
    POIs are the core of this system. They are literally points
      of interest, and will have name, image and description (Other
      fields MAY be added in the future or via plug-in).
    """

    # Timestamp fields.
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('Created On'))
    updated_on = models.DateTimeField(auto_now=True, verbose_name=_('Updated On'))
    # Public (display) data: name and short description are mandatory fields,
    #   but long descriptions and image are not.
    name = models.CharField(max_length=80, verbose_name=_('Name'))
    description = models.TextField(max_length=512, verbose_name=_('Description'))
    picture = models.ImageField(upload_to='pictures', blank=True, null=True, verbose_name=_('Picture'))
    # Filtering data (by category or location).
    location = PointField(verbose_name=_('Location'))
    categories = models.ManyToManyField(Category, verbose_name=_('Categories'))
    # Internal fields.
    internal_notes = models.TextField(null=True, blank=True, verbose_name=_('Internal Notes'),
                                      help_text=_('These notes are only useful here, in the admin panel, and '
                                                  'are never revealed as public data. Use this space to take '
                                                  'all the notes you need about this POI.'))
    # Fields for deleted POI (to check in database only).
    deleted = models.BooleanField(default=False, editable=False)
    deleted_by = models.ForeignKey('User', editable=False, null=True, on_delete=models.SET_NULL)

    objects = POIQuerySet.as_manager()

    class Meta:
        verbose_name = _('POI')
        verbose_name_plural = _('POIs')
