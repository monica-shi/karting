# Generated by Django 4.2.7 on 2023-11-25 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0003_session_temp_session_track_conditions_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session',
            old_name='gear',
            new_name='sprocket_size',
        ),
        migrations.AddField(
            model_name='session',
            name='engine_driver_size',
            field=models.IntegerField(choices=[(10, 10), (11, 11), (12, 12), (13, 13)], default=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chassis',
            name='brand',
            field=models.CharField(choices=[('CompKart', 'CompKart'), ('BirelArt', 'BirelArt'), ('Kosmic', 'Kosmic'), ('Red Speed', 'Red Speed'), ('Tony Kart', 'Tony Kart'), ('KartRepublic', 'Kart Republic'), ('SODI', 'SODI Kart')], max_length=200),
        ),
        migrations.AlterField(
            model_name='chassis',
            name='year',
            field=models.IntegerField(blank=True, choices=[(2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023)], default=2023, help_text='Enter the year the chassis model came out.', null=True),
        ),
    ]
