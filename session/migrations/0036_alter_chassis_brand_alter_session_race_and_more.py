# Generated by Django 4.2.7 on 2024-01-22 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0035_remove_session_time_alter_chassis_brand_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chassis',
            name='brand',
            field=models.CharField(choices=[('CompKart', 'CompKart'), ('BirelArt', 'BirelArt'), ('Red Speed', 'Red Speed'), ('Kosmic', 'Kosmic'), ('KartRepublic', 'Kart Republic'), ('SODI', 'SODI Kart'), ('Tony Kart', 'Tony Kart')], max_length=200),
        ),
        migrations.AlterField(
            model_name='session',
            name='race',
            field=models.CharField(choices=[('Stars', 'Stars'), ('NEKC', 'Northeast Karting Championship'), ('SKUSA', 'Super Karts USA'), ('USPKS', 'US Pro Karting Series'), ('WSK', 'World Series Karting'), ('Italian Championship', 'Italian Championship'), ('None', 'None'), ('Rotax', 'Rotax Races'), ('RokCup', 'ROK Cup')], help_text='Choose "none" if this is a practice weekend', max_length=100),
        ),
        migrations.AlterField(
            model_name='session',
            name='session_type',
            field=models.CharField(choices=[('Pre-final', 'Pre-final race'), ('Heat', 'Heat race'), ('Qualifying', 'Qualifying Practice'), ('Final', 'Final race'), ('Practice', 'General Practice')], default='Practice', max_length=20),
        ),
    ]
