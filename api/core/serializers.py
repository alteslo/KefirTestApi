from rest_framework import serializers

from core.models import Cities, MyUser


class UserSerializer(serializers.ModelSerializer):
    '''Данные о текущем пользователе'''

    class Meta:
        model = MyUser
        fields = [
            'first_name',
            'last_name',
            'other_name',
            'email',
            'phone',
            'birthday',
            'is_admin'
        ]


class CitiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cities
        fields = '__all__'
