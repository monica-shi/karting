import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Chassis, Engine

class SessionForm(forms.Form):
    # renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    # # chassis
    # chassis_brand = forms.CharField()
    # chassis_year = forms.DateField()
    # chassis_model = forms.CharField()
    # chassis_description = forms.CharField()
    #
    # # engine detail
    # engine_model = forms.CharField()
    # engine_nickname= forms.CharField()
    # engine_serial = forms.IntegerField()

    # session detail
    session_date = forms.DateField()
    session_time = forms.TimeField()
    session_track = forms.CharField()
    # chassis_choices = [(str(c), c) for c in Chassis.objects.all()]
    # session_chassis = forms.ChoiceField(chassis_choices)
    # engine_choices = [(str(e), e) for e in Engine.objects.all()]
    # session_engine = forms.ChoiceField(engine_choices)


    # def clean_renewal_date(self):
    #     data = self.cleaned_data['renewal_date']
    #
    #     # Check if a date is not in the past.
    #     if data < datetime.date.today():
    #         raise ValidationError(_('Invalid date - renewal in past'))
    #
    #     # Check if a date is in the allowed range (+4 weeks from today).
    #     if data > datetime.date.today() + datetime.timedelta(weeks=4):
    #         raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
    #
    #     # Remember to always return the cleaned data.
    #     return data
