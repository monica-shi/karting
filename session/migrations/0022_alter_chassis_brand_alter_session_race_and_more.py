# Generated by Django 4.2.7 on 2024-01-16 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0021_session_carburetor_alter_chassis_brand_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chassis',
            name='brand',
            field=models.CharField(choices=[('Kosmic', 'Kosmic'), ('KartRepublic', 'Kart Republic'), ('Tony Kart', 'Tony Kart'), ('Red Speed', 'Red Speed'), ('SODI', 'SODI Kart'), ('BirelArt', 'BirelArt'), ('CompKart', 'CompKart')], max_length=200),
        ),
        migrations.AlterField(
            model_name='session',
            name='race',
            field=models.CharField(choices=[('RokCup', 'ROK Cup'), ('Italian Championship', 'Italian Championship'), ('Rotax', 'Rotax Races'), ('NEKC', 'Northeast Karting Championship'), ('USPKS', 'US Pro Karting Series'), ('Stars', 'Stars'), ('WSK', 'World Series Karting'), ('SKUSA', 'Super Karts USA')], max_length=100),
        ),
        migrations.AlterField(
            model_name='session',
            name='session_type',
            field=models.CharField(choices=[('Final', 'Final race'), ('Pre-final', 'Pre-final race'), ('Qualifying', 'Qualifying Practice'), ('Heat', 'Heat race'), ('Practice', 'General Practice')], default='Practice', max_length=20),
        ),
    ]
