# Generated by Django 4.2.7 on 2024-01-06 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0019_alter_chassis_brand_alter_session_race_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='carburetor',
        ),
        migrations.AddField(
            model_name='session',
            name='rear_axle_type',
            field=models.CharField(help_text='The type of the real axle', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='session',
            name='rear_width',
            field=models.IntegerField(blank=True, help_text='Rear width in mm', null=True),
        ),
        migrations.AddField(
            model_name='session',
            name='tire_pressure_fl_hot',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Pressure of the front left tire', max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='session',
            name='tire_pressure_fr_hot',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Pressure of the front right tire', max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='session',
            name='tire_pressure_rl_hot',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Pressure of the rear left tire', max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='session',
            name='tire_pressure_rr_hot',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Pressure of the rear right tire', max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='chassis',
            name='brand',
            field=models.CharField(choices=[('SODI', 'SODI Kart'), ('CompKart', 'CompKart'), ('BirelArt', 'BirelArt'), ('KartRepublic', 'Kart Republic'), ('Kosmic', 'Kosmic'), ('Tony Kart', 'Tony Kart'), ('Red Speed', 'Red Speed')], max_length=200),
        ),
        migrations.AlterField(
            model_name='session',
            name='race',
            field=models.CharField(choices=[('RokCup', 'ROK Cup'), ('WSK', 'World Series Karting'), ('SKUSA', 'Super Karts USA'), ('USPKS', 'US Pro Karting Series'), ('NEKC', 'Northeast Karting Championship'), ('Italian Championship', 'Italian Championship'), ('Stars', 'Stars'), ('Rotax', 'Rotax Races')], max_length=100),
        ),
        migrations.AlterField(
            model_name='session',
            name='session_type',
            field=models.CharField(choices=[('Qualifying', 'Qualifying Practice'), ('Pre-final', 'Pre-final race'), ('Final', 'Final race'), ('Practice', 'General Practice'), ('Heat', 'Heat race')], default='Practice', max_length=20),
        ),
    ]
