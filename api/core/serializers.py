from core.models import Cities, MyUser
from rest_framework import serializers


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
        fields = ('city', )


class PrivateGETUsersSerializer(serializers.ModelSerializer):
    '''Сериализатор данных о всех пользователях доступный админу'''
    city = serializers.SlugRelatedField(
        slug_field="city", queryset=Cities.objects.all(), required=False
    )
    password = serializers.CharField(write_only=True)

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
        optional_fields = ('city', 'password')

    def create(self, validated_data):
        instance = MyUser.objects.create_user(**validated_data)
        return instance


class PrivateLISTUsersSerializer(serializers.ModelSerializer):
    '''Сериализатор кратких данных пользователя доступных админу'''

    class Meta:
        model = MyUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'email'
        ]
