from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from core.models import MyUser


class MyUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = MyUser
        fields = UserCreationForm.Meta.fields


class MyUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = MyUser
        fields = UserChangeForm.Meta.fields
