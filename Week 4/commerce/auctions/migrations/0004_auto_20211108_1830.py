# Generated by Django 3.2.8 on 2021-11-08 10:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20211107_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='watchers',
            field=models.ManyToManyField(blank=True, null=True, related_name='watched_listings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='listing_won', to=settings.AUTH_USER_MODEL),
        ),
    ]