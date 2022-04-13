from rest_framework import serializers

from core.models import Cities, MyUser


class UsersSerializer(serializers.ModelSerializer):
    '''Сериализатор данных о всех пользователях'''

    class Meta:
        model = MyUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'email'
        ]


class CurrentUsersSerializer(serializers.ModelSerializer):
    '''Сериализатор данных доступных пользователю о самом себе'''

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
