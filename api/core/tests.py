from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import MyUser

# class UserFactory(factory.Factory):
#     class Meta:
#         model = MyUser
#     first_name = factory.Faker('first_name')
#     email = factory.Faker('email')
#     is_admin = False
#     password = factory.Faker('password')


class MyUserTests(APITestCase):
    def setUp(self):
        fake = Faker()
        MyUser.objects.create_user(
            email='aaa@net.com', is_admin=True, password='0112358')
        for _ in range(10):
            MyUser.objects.create_user(
                email=fake.email(),
                password=fake.password(),
                is_admin=False,
                first_name=fake.first_name()
            )

    def test_get_general_users_information(self):

        self.client.login(username='aaa@net.com', password='0112358')

        url = reverse('general_users_information')  # + '?page=4&size=2'
        print(f'{url=}')
        response = self.client.get(url, format='json')
        results = response.json()
        print(f'\n{results=}\n')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MyUser.objects.count(), 11)
        # self.assertEqual(MyUser.objects.get().name, 'DabApps')
