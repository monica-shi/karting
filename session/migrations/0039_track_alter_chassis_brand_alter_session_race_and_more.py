# Generated by Django 4.2.7 on 2024-04-01 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0038_alter_chassis_brand_alter_session_race_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the track', max_length=100)),
                ('country', models.CharField(help_text='The country of the track', max_length=50)),
                ('website', models.URLField(null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='chassis',
            name='brand',
            field=models.CharField(choices=[('Arrow', 'Arrow Racing Karts'), ('BirelArt', 'BirelArt'), ('CRG', 'CRG'), ('CompKart', 'CompKart'), ('EnergyKart', 'Energy Kart'), ('KartRepublic', 'Kart Republic'), ('Kosmic', 'Kosmic'), ('LandoNorrisKart', 'Lando Norris Kart'), ('Parolin', 'Parolin'), ('Red Speed', 'Red Speed'), ('SODI', 'SODI Kart'), ('Tony Kart', 'Tony Kart')], max_length=200),
        ),
        migrations.AlterField(
            model_name='session',
            name='race',
            field=models.CharField(choices=[('SKUSA', 'Super Karts USA'), ('USPKS', 'US Pro Karting Series'), ('NEKC', 'Northeast Karting Championship'), ('RokCup', 'ROK Cup'), ('Italian Championship', 'Italian Championship'), ('None', 'None'), ('WSK', 'World Series Karting'), ('Rotax', 'Rotax Races'), ('Stars', 'Stars')], help_text='Choose "none" if this is a practice weekend', max_length=100),
        ),
        migrations.AlterField(
            model_name='session',
            name='session_type',
            field=models.CharField(choices=[('Pre-final', 'Pre-final race'), ('Qualifying', 'Qualifying Practice'), ('Final', 'Final race'), ('Practice', 'General Practice'), ('Heat', 'Heat race')], default='Practice', max_length=20),
        ),
    ]
