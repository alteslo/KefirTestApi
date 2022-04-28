from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import MyUser


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

        url = reverse('general_users_information')
        response = self.client.get(url, format='json')
        pagination_data = response.json().get('meta').get('pagination')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MyUser.objects.count(), 11)
        self.assertEqual(pagination_data.get('page'), 1)
        self.assertEqual(pagination_data.get('size'), 3)

        PAGE = 4
        SIZE = 2
        url += f'?page={PAGE}&size={SIZE}'
        response = self.client.get(url, format='json')
        pagination_data = response.json().get('meta').get('pagination')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(pagination_data.get('page'), PAGE)
        self.assertEqual(pagination_data.get('size'), SIZE)

        data_fields = [
            field for field in response.json().get('data')[0].keys()
        ]
        self.assertEqual(
            data_fields, ['id', 'first_name', 'last_name', 'email']
        )

    def test_get_general_users_information_unauth(self):

        self.client.logout()

        url = reverse('general_users_information')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
