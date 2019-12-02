"""
Notes for future self: I know I should use the Tracked models I created for this purpose. Perhaps.

BUT I did not port it to Python 3 yet, and the former namespace format have a bug in Python 3.6.
"""


from django.db import models
from django.utils.translation import ugettext_lazy as _


class SoftDeletedQueryset(models.QuerySet):

    def all(self):
        """
        Excludes the marked-as-deleted records.
        :return: A base queryset, excluding the deleted ones.
        """

        # If at least one of the two fields is null, it will count
        #   as deleted and not included in the regular queryset.
        return self.filter(deleted=False, deleted_by__isnull=True)


class SoftDeleted(models.Model):
    """
    Marks creation and deletion of records logically. Also marks responsible user,
      if the case, of the deletion.
    """

    # Timestamp fields.
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('Created On'))
    updated_on = models.DateTimeField(auto_now=True, verbose_name=_('Updated On'))
    # Deletion fields (to check in database only).
    deleted = models.BooleanField(default=False, editable=False)
    deleted_by = models.ForeignKey('User', editable=False, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class Described(SoftDeleted):
    """
    Adds some description fields to the records. Useful for publicly available
      data, like regions and POIs.
    """

    # Public (display) data.
    name = models.CharField(max_length=80, verbose_name=_('Name'))
    description = models.TextField(max_length=512, verbose_name=_('Description'))
    # Internal fields.
    internal_notes = models.TextField(null=True, blank=True, verbose_name=_('Internal Notes'),
                                      help_text=_('These notes are only useful here, in the admin panel, and '
                                                  'are never revealed as public data. Use this space to take '
                                                  'all the notes you need about this POI.'))

    class Meta:
        abstract = True
