# Generated by Django 2.2.4 on 2019-08-29 22:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wtfapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='poi',
            options={'permissions': (('manage_country_pois', 'Can manage POIs in specific countries'), ('manage_region_pois', 'Can manage POIs in specific regions')), 'verbose_name': 'POI', 'verbose_name_plural': 'POIs'},
        ),
    ]
