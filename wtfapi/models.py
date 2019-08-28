from django.db import models
from django.contrib.gis.db.models import PointField


# Create your models here.
class POI(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=80)
    short_description = models.TextField(max_length=512)
    long_description = models.TextField()
    location = PointField()
    # Other fields may be added later, like picture(s)


# You can query like: POI.objects.filter(location__distance_lte=(
#     somePoint, e.g. POI.objects.get(pk=1).location, somePositiveIntDistance
# ))

# You can also annotate distances, like: POI.objects.annotate(distance=Distance('location', pnt))
