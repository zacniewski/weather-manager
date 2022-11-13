# Generated by Django 4.1.3 on 2022-11-13 15:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="WeatherData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("location", models.CharField(max_length=100)),
                ("latitude", models.CharField(max_length=30)),
                ("longitude", models.CharField(max_length=30)),
                ("local_time", models.CharField(max_length=30)),
                ("pressure_mb", models.CharField(max_length=30)),
                ("wind_kph", models.CharField(max_length=30)),
                ("wind_dir", models.CharField(max_length=30)),
                ("timezone", models.CharField(max_length=30)),
                ("cloudiness", models.CharField(max_length=30)),
                ("humidity", models.CharField(max_length=30)),
                ("precipitation", models.CharField(max_length=30)),
                ("condition_icon", models.URLField(max_length=100)),
                ("country", models.CharField(max_length=30)),
                ("temperature", models.CharField(max_length=10)),
                ("feels_like", models.CharField(max_length=10)),
                ("condition", models.CharField(max_length=30)),
                ("created", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="FavouriteLocation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("location", models.CharField(max_length=100)),
                ("created", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
