# Generated by Django 4.2.7 on 2024-01-21 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0032_alter_chassis_brand_alter_session_race_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chassis',
            name='brand',
            field=models.CharField(choices=[('Red Speed', 'Red Speed'), ('Kosmic', 'Kosmic'), ('CompKart', 'CompKart'), ('SODI', 'SODI Kart'), ('Tony Kart', 'Tony Kart'), ('BirelArt', 'BirelArt'), ('KartRepublic', 'Kart Republic')], max_length=200),
        ),
        migrations.AlterField(
            model_name='session',
            name='race',
            field=models.CharField(choices=[('WSK', 'World Series Karting'), ('None', 'None'), ('RokCup', 'ROK Cup'), ('Italian Championship', 'Italian Championship'), ('Stars', 'Stars'), ('Rotax', 'Rotax Races'), ('NEKC', 'Northeast Karting Championship'), ('USPKS', 'US Pro Karting Series'), ('SKUSA', 'Super Karts USA')], help_text='Choose "none" if this isa practice weekend', max_length=100),
        ),
        migrations.AlterField(
            model_name='session',
            name='session_type',
            field=models.CharField(choices=[('Heat', 'Heat race'), ('Qualifying', 'Qualifying Practice'), ('Pre-final', 'Pre-final race'), ('Practice', 'General Practice'), ('Final', 'Final race')], default='Practice', max_length=20),
        ),
    ]