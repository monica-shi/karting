from django.contrib import admin
from .models import Chassis, Engine, Track, Session


# Register your models here.


@admin.register(Chassis)
class ChassisAdmin(admin.ModelAdmin):
    list_display = ('brand', 'year', 'model')


@admin.register(Engine)
class EngineAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model', 'nickname', 'serial_num')


@admin.register(Track)
class EngineAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'website')


# are inlines/tubularline needed here?
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_filter = ('date', 'track', 'race')
    # add weather when implemented; is filtering by date necessary? or does it by default sort by most recent?

    fieldsets = (
        (None, {
            'fields': (('date', 'session_time'), 'race', 'track', 'track_conditions', 'weather', 'temp')
        }),
        ('Kart Setup', {
            'fields': (('chassis', 'engine', 'carburetor'),
                       ('high_jetting', 'low_jetting'),
                       ('castor', 'camber'),
                       ('engine_driver_size', 'sprocket_size'),
                       ('tire', 'rim', 'tire_pressure_fl', 'tire_pressure_fr', 'tire_pressure_rl', 'tire_pressure_rr'))
        }),  # add another fieldset for times when those fields are implemented in models
        ('Session Result', {
            'fields': (
                ('lap_time1', 'lap_time2', 'lap_time3'),
                ('rpm_max1', 'rpm_max2', 'rpm_max3'),
                ('rpm_min1', 'rpm_min2', 'rpm_min3'),
                ('egt_max1', 'egt_max2', 'egt_max3'),
                ('egt_min1', 'egt_min2', 'egt_min3'),
                ('speed_max1', 'speed_max2', 'speed_max3'),
                ('speed_min1', 'speed_min2', 'speed_min3')
            )
        }),
    )
