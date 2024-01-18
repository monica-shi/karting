from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

import datetime


BRAND_CHOICES = {
    ('Tony Kart', 'Tony Kart'),
    ('Kosmic', 'Kosmic'),
    ('Red Speed', 'Red Speed'),
    ('KartRepublic', 'Kart Republic'),
    ('SODI', 'SODI Kart'),
    ('CompKart', 'CompKart'),
    ('BirelArt', 'BirelArt'),
}


def year_choices():
    return [(r, r) for r in range(2010, datetime.date.today().year+1)]


def current_year():
    return datetime.date.today().year


class Chassis(models.Model):
    """Model representing a chassis"""
    brand = models.CharField(blank=False, choices=BRAND_CHOICES, max_length=200)
    year = models.IntegerField(blank=True, null=True,choices=year_choices(), default=current_year(),
                               help_text='Enter the year the chassis model came out.')
    model = models.CharField(blank=True, null=True, max_length=200, help_text='Enter prototype, if applicable')
    description = models.TextField(blank=True, null=True, help_text='Enter a description of how this '
                                                                    'chassis behaves.')

    def __str__(self):
        return str(self.brand) + "-" + str(self.year) + '-' + str(self.model)

    def get_absolute_url(self):
        """Returns the URL to access a particular chassis instance"""
        return reverse('chassis-detail', args=[str(self.id)])


class Engine(models.Model):
    """Model representing an engine"""
    manufacturer = models.CharField(blank=False, max_length=200, help_text='IAME, Rotax, etc.')
    model = models.CharField(blank=False, max_length=200, help_text='Rok, X30, etc.')
    nickname = models.CharField(blank=True, null=True, max_length=200,
                                help_text='Enter a nickname to help quickly identify '
                                          'specific engine')
    serial_num = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.nickname:
            return self.nickname
        else:
            return '_'.join([str(self.model), str(self.serial_num)])

    def get_absolute_url(self):
        return reverse('engine-detail', args=[str(self.id)])


RACE_CHOICES = {
    ('None', 'None'),
    ('SKUSA', 'Super Karts USA'),
    ('USPKS', 'US Pro Karting Series'),
    ('RokCup', 'ROK Cup'),
    ('NEKC', 'Northeast Karting Championship'),
    ('Stars', 'Stars'),
    ('Italian Championship', 'Italian Championship'),
    ('WSK', 'World Series Karting'),
    ('Rotax', 'Rotax Races')
}

SESSION_TYPES = {
    ('Practice', 'General Practice'),
    ('Qualifying', 'Qualifying Practice'),
    ('Heat', 'Heat race'),
    ('Pre-final', 'Pre-final race'),
    ('Final', 'Final race'),
}


class Session(models.Model):  # make sure blank=True for necessary fields
    """Model representing a test session"""

    date = models.DateField(blank=False)
    time = models.TimeField(blank=False, auto_now=True, auto_now_add=False)
    race = models.CharField(blank=False, max_length=100, choices=RACE_CHOICES, help_text='Choose "none" if this is'
                                                                                         'a practice weekend')
    session_type = models.CharField(blank=False, null=False, default='Practice', max_length=20, choices=SESSION_TYPES)
    track = models.CharField(blank=False, max_length=200)
    track_conditions = models.TextField(blank=True, null=True, help_text='(Optional) Please enter a brief description '
                                                                         'of the track conditions.')
    weather = models.CharField(blank=False, default='sunny', max_length=200, help_text='Sunny, cloudy, rainy, pouring, etc.')
    temp = models.IntegerField(blank=False, null=True, help_text='Please enter the temperature in Fahrenheit.')
    # air_read = # how to install??
    # gear range might need multiple for shifter karts
    chassis = models.ForeignKey('Chassis', on_delete=models.PROTECT, null=True)
    engine = models.ForeignKey('Engine', on_delete=models.PROTECT, null=True)
    engine_driver_size = models.IntegerField(blank=False, choices=[(r, r) for r in range(10, 14)])
    sprocket_size = models.IntegerField(blank=True, help_text='See below for shifter kart sprocket sizes')
    sprocket_range = models.CharField(blank=True, help_text='Please enter a sprocket range if running a shifter kart.'
                                                            'Leave blank otherwise')
    tire = models.CharField(blank=False, max_length=200, help_text='Enter a brand of tire.')
    tire_type = models.CharField(blank=True, null=True, default='slick', max_length=200, help_text='Wets or slick?')
    rim = models.CharField(blank=False, max_length=200, help_text='Enter a rim type.')
    high_jetting = models.IntegerField(blank=True, null=True)
    low_jetting = models.IntegerField(blank=True, null=True,
                                      help_text='Low jetting for Tillotson carb (in minutes)'
                                                ' or main jet size for Dellorto carb')
    castor = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=2)
    camber = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=2)
    rear_axle_type = models.CharField(blank=False, null=True, max_length=10,
                                      help_text='The type of the rear axle')
    rear_width = models.IntegerField(blank=True, null=True, help_text='Rear width in mm')
    tire_pressure_fr = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2,
                                           help_text='Pressure of the front right tire')
    tire_pressure_fl = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2,
                                           help_text='Pressure of the front left tire')
    tire_pressure_rl = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2,
                                           help_text='Pressure of the rear left tire')
    tire_pressure_rr = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2,
                                           help_text='Pressure of the rear right tire')

    carburetor = models.CharField(blank=True, null=True, max_length=200, help_text='Type of carb.')

    lap_time1 = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=3,
                                    help_text='The best lap time, in seconds')
    lap_time2 = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=3,
                                    help_text='The second best lap tim, in seconds')
    lap_time3 = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=3,
                                    help_text='The third best lap time, in seconds')
    rpm_max1 = models.IntegerField(blank=True, null=True, help_text='Max RPM of the best lap')
    rpm_max2 = models.IntegerField(blank=True, null=True, help_text='Max RPM of the second best lap')
    rpm_max3 = models.IntegerField(blank=True, null=True, help_text='Max RPM of the third best lap')
    rpm_min1 = models.IntegerField(blank=True, null=True, help_text='min RPM of the best lap')
    rpm_min2 = models.IntegerField(blank=True, null=True, help_text='min RPM of the second best lap')
    rpm_min3 = models.IntegerField(blank=True, null=True, help_text='min RPM of the third best lap')
    egt_max1 = models.IntegerField(blank=True, null=True, help_text='Max EGT of the best lap')
    egt_max2 = models.IntegerField(blank=True, null=True, help_text='Max EGT of the second best lap')
    egt_max3 = models.IntegerField(blank=True, null=True, help_text='Max EGT of the third best lap')
    egt_min1 = models.IntegerField(blank=True, null=True, help_text='min EGT of the best lap')
    egt_min2 = models.IntegerField(blank=True, null=True, help_text='min EGT of the second best lap')
    egt_min3 = models.IntegerField(blank=True, null=True, help_text='min EGT of the third best lap')
    speed_max1 = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2,
                                     help_text='The max speed of the best lap')
    speed_max2 = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2,
                                     help_text='The max speed of the second best lap')
    speed_max3 = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2,
                                     help_text='The max speed of the third best lap')
    speed_min1 = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2,
                                     help_text='The min speed of the best lap')
    speed_min2 = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2,
                                     help_text='The min speed of the second best lap')
    speed_min3 = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2,
                                     help_text='The min speed of the third best lap')

    tire_pressure_fr_hot = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2,
                                               help_text='Pressure of the front right tire')
    tire_pressure_fl_hot = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2,
                                               help_text='Pressure of the front left tire')
    tire_pressure_rl_hot = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2,
                                               help_text='Pressure of the rear left tire')
    tire_pressure_rr_hot = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2,
                                               help_text='Pressure of the rear right tire')
    session_general_notes = models.TextField(blank=True, null=True, help_text='Driver spun, stopped/started raining, '
                                                                              'should have used bigger sprocket, etc.')

    def __str__(self):
        return '-'.join([str(self.date), str(self.time), str(self.track)])

    def get_absolute_url(self):
        return reverse('session-detail', args=[str(self.id)])
