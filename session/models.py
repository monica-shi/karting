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


class Session(models.Model):  # make sure blank=True for necessary fields
    """Model representing a test session"""

    date = models.DateField(blank=False)
    weather = models.CharField(blank=False, default='sunny', max_length=200, help_text='Sunny, cloudy, rainy, pouring, etc.')
    temp = models.IntegerField(blank=True, null=True, help_text='Please enter the temperature in Fahrenheit.')
    track_conditions = models.TextField(blank=True, null=True, help_text='Please enter a brief description of the'
                                                                         'track conditions.')
    # air_read = # how to install??
    # gear range might need multiple for shifter karts
    chassis = models.ForeignKey('Chassis', on_delete=models.PROTECT, null=True)
    engine = models.ForeignKey('Engine', on_delete=models.PROTECT, null=True)
    gear = models.IntegerField(blank=False)
    tire = models.CharField(blank=False, max_length=200, help_text='Enter a brand of tire.')
    rim = models.CharField(blank=False, max_length=200, help_text='Enter a rim type.')
    jet_size = models.IntegerField(blank=False)
    castor = models.IntegerField(blank=True, null=True)
    camber = models.IntegerField(blank=True, null=True)
    tire_pressure = models.CharField(blank=False, max_length=200)  # can't do integer bc sometimes have floats
    carburetor = models.CharField(blank=True, null=True, max_length=200, help_text='Type of carb.')
    track = models.CharField(blank=False, max_length=200)

    # need time1, time2, time2, max RPM1, max RPM2, max RPM3, and engine temps

    # add all return statements !
    def __str__(self):
        return self.date

    def get_absolute_url(self):
        return reverse('session-detail', args=[str(self.id)])
