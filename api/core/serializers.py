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


class CurrentUsersPUTCHSerializer(serializers.ModelSerializer):
    '''Сериализатор данных доступных пользователю для редактирования'''

    class Meta:
        model = MyUser
        fields = [
            'first_name',
            'last_name',
            'other_name',
            'email',
            'phone',
            'birthday',
        ]


class CitiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cities
        fields = '__all__'


class PrivateUsersSerializer(serializers.ModelSerializer):
    '''Сериализатор данных о всех пользователях доступный админу'''
    city = CitiesSerializer(required=False)

    class Meta:
        model = MyUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'other_name',
            'email',
            'phone',
            'birthday',
            'city',
            'additional_info',
            'is_admin',
            'password'
        ]
        # optional_fields = ["city"]


class PrivateGETUsersSerializer(serializers.ModelSerializer):
    '''Сериализатор кратких данных пользователя доступных админу'''

    class Meta:
        model = MyUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'email'
        ]
