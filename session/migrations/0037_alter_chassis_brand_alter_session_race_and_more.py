# Generated by Django 4.2.7 on 2024-01-23 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0036_alter_chassis_brand_alter_session_race_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chassis',
            name='brand',
            field=models.CharField(choices=[('Kosmic', 'Kosmic'), ('SODI', 'SODI Kart'), ('CompKart', 'CompKart'), ('Tony Kart', 'Tony Kart'), ('KartRepublic', 'Kart Republic'), ('BirelArt', 'BirelArt'), ('Red Speed', 'Red Speed')], max_length=200),
        ),
        migrations.AlterField(
            model_name='session',
            name='race',
            field=models.CharField(choices=[('SKUSA', 'Super Karts USA'), ('WSK', 'World Series Karting'), ('None', 'None'), ('USPKS', 'US Pro Karting Series'), ('Stars', 'Stars'), ('RokCup', 'ROK Cup'), ('NEKC', 'Northeast Karting Championship'), ('Italian Championship', 'Italian Championship'), ('Rotax', 'Rotax Races')], help_text='Choose "none" if this is a practice weekend', max_length=100),
        ),
        migrations.AlterField(
            model_name='session',
            name='session_type',
            field=models.CharField(choices=[('Pre-final', 'Pre-final race'), ('Practice', 'General Practice'), ('Heat', 'Heat race'), ('Final', 'Final race'), ('Qualifying', 'Qualifying Practice')], default='Practice', max_length=20),
        ),
    ]
