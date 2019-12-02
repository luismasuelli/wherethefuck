# Generated by Django 2.2.4 on 2019-12-02 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wtfapi', '0004_auto_20191202_2253'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='province',
            options={'permissions': (('manage_country_provinces', 'Can manage provinces in specific countries'),), 'verbose_name': 'Province', 'verbose_name_plural': 'Provinces'},
        ),
        migrations.AlterField(
            model_name='poi',
            name='categories',
            field=models.ManyToManyField(blank=True, to='category.Category', verbose_name='Categories'),
        ),
    ]
