from rest_framework import serializers

from core.models import Cities, MyUser


class UsersSerializer(serializers.ModelSerializer):
    '''Данные о текущем пользователе'''

    class Meta:
        model = MyUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'email'
        ]


class CitiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cities
        fields = '__all__'
