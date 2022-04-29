from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import MyUser


class MyUserTests(APITestCase):
    def setUp(self):
        fake = Faker()
        MyUser.objects.create_user(
            email='aaa@net.com',
            is_admin=True,
            password='0112358',
            birthday='2022-04-29')
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

    def test_get_current_user_information(self):

        self.client.login(username='aaa@net.com', password='0112358')

        url = reverse('current_user_information')
        response = self.client.get(url, format='json')
        current_user_information = {
            'first_name': '',
            'last_name': '',
            'other_name': '',
            'email': 'aaa@net.com',
            'phone': '',
            'birthday': '2022-04-29',
            'is_admin': True
        }
        self.assertEqual(response.json(), current_user_information)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_current_user_information_unauth(self):

        self.client.logout()

        url = reverse('current_user_information')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_putch_current_user_information(self):
        user = MyUser.objects.get(email='aaa@net.com')
        
        response = client.get('http://testserver/homepage/')
        assert response.status_code == 200
        csrftoken = response.cookies['csrftoken']

        # Interact with the API.
        response = client.post('http://testserver/organisations/', json={
            'name': 'MegaCorp',
            'status': 'active'
        }, headers={'X-CSRFToken': csrftoken})
assert response.status_code == 200
        
        
        self.client.login(username='aaa@net.com', password='0112358')
        url = f'/api/user/users/{user.id}/'

        data = {
            'first_name': '',
            'last_name': '',
            'other_name': '',
            'phone': '',
            'birthday': '2022-04-29'
        }

        response = self.client.patch(url, data, format='json')
        print(f'{response}')

        # response = self.client.get(url, format='json')
        # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
