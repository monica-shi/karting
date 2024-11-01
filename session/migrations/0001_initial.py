# Generated by Django 4.2.2 on 2023-06-22 02:48

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Chassis",
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
                ("brand", models.CharField(max_length=200)),
                (
                    "year",
                    models.IntegerField(
                        blank=True,
                        help_text="Enter the year the chassis model came out.",
                        null=True,
                    ),
                ),
                (
                    "model",
                    models.CharField(
                        blank=True,
                        help_text="Enter prototype, if applicable",
                        max_length=200,
                        null=True,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Enter a description of how this chassis behaves.",
                        null=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Engine",
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
                (
                    "manufacturer",
                    models.CharField(help_text="IAME, Rotax, etc.", max_length=200),
                ),
                ("model", models.CharField(help_text="Rok, X30, etc.", max_length=200)),
                (
                    "nickname",
                    models.CharField(
                        blank=True,
                        help_text="Enter a nickname to help quickly identify specific engine",
                        max_length=200,
                        null=True,
                    ),
                ),
                ("serial_num", models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Session",
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
                ("date", models.DateField()),
                ("gear", models.IntegerField()),
                (
                    "tire",
                    models.CharField(
                        help_text="Enter a brand of tire.", max_length=200
                    ),
                ),
                ("rim", models.CharField(help_text="Enter a rim type", max_length=200)),
                ("jet_size", models.IntegerField()),
                ("castor", models.IntegerField(blank=True, null=True)),
                ("camber", models.IntegerField(blank=True, null=True)),
                ("tire_pressure", models.CharField(max_length=200)),
                (
                    "carburetor",
                    models.CharField(
                        blank=True, help_text="Type of carb.", max_length=200, null=True
                    ),
                ),
                ("track", models.CharField(max_length=200)),
            ],
        ),
    ]
