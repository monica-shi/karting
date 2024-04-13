from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


class SignupForm(UserCreationForm):

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            default_group = Group.objects.get(name='default')
            default_group.user_set.add(user)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']