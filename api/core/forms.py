from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from core.models import MyUser


class MyUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = MyUser
        fields = UserCreationForm.Meta.fields + ('city', 'birthday',)


class MyUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = MyUser
        fields = UserChangeForm.Meta.fields
