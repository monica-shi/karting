from django.contrib import admin
from .models import Chassis, Engine, Session


# Register your models here.


@admin.register(Chassis)
class ChassisAdmin(admin.ModelAdmin):
    list_display = ('brand', 'year', 'model')


@admin.register(Engine)
class EngineAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model', 'nickname', 'serial_num')


# are inlines/tubularline needed here?
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_filter = ('date', 'track')
    # add weather when implemented; is filtering by date necessary? or does it by default sort by most recent?

    fieldsets = (
        (None, {
            'fields': ('date', 'weather', 'temp', 'track_conditions', 'track')
        }),
        ('Kart Setup', {
            'fields': (('chassis', 'engine'), ('carburetor', 'jet_size'), 'gear', ('tire', 'rim', 'tire_pressure'),
                       ('castor', 'camber'))
        }),  # add another fieldset for times when those fields are implemented in models
    )
