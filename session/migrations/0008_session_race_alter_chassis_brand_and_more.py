# Generated by Django 4.2.7 on 2023-11-26 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0007_remove_session_jet_size_alter_chassis_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='race',
            field=models.CharField(choices=[('Italian Championship', 'Italian Championship'), ('WSK', 'World Series Karting'), ('Stars', 'Stars'), ('USPKS', 'US Pro Karting Series'), ('Rotax', 'Rotax Races'), ('SKUSA', 'Super Karts USA'), ('NEKC', 'Northeast Karting Championship'), ('RokCup', 'ROK Cup')], default='SKUSA', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chassis',
            name='brand',
            field=models.CharField(choices=[('Kosmic', 'Kosmic'), ('Red Speed', 'Red Speed'), ('KartRepublic', 'Kart Republic'), ('SODI', 'SODI Kart'), ('CompKart', 'CompKart'), ('Tony Kart', 'Tony Kart'), ('BirelArt', 'BirelArt')], max_length=200),
        ),
        migrations.AlterField(
            model_name='session',
            name='camber',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='castor',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
    ]