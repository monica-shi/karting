from django import forms
from .models import Session


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        exclude = ('user',)

    def as_table(self):
        return super().as_table()