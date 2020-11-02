from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import MoovieUser


class MoovieUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = MoovieUser
        fields = ('email',)


class MoovieUserChangeForm(UserChangeForm):

    class Meta:
        model = MoovieUser
        fields = ('email',)