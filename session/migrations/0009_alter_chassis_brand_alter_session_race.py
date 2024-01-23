# Generated by Django 4.2.7 on 2024-01-01 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0008_session_race_alter_chassis_brand_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chassis',
            name='brand',
            field=models.CharField(choices=[('Kosmic', 'Kosmic'), ('SODI', 'SODI Kart'), ('CompKart', 'CompKart'), ('Tony Kart', 'Tony Kart'), ('BirelArt', 'BirelArt'), ('KartRepublic', 'Kart Republic'), ('Red Speed', 'Red Speed')], max_length=200),
        ),
        migrations.AlterField(
            model_name='session',
            name='race',
            field=models.CharField(choices=[('Italian Championship', 'Italian Championship'), ('WSK', 'World Series Karting'), ('RokCup', 'ROK Cup'), ('Rotax', 'Rotax Races'), ('Stars', 'Stars'), ('USPKS', 'US Pro Karting Series'), ('SKUSA', 'Super Karts USA'), ('NEKC', 'Northeast Karting Championship')], max_length=100),
        ),
    ]
