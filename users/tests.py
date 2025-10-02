from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from . import models


class UserRegistrationViewTestCase(TestCase):
    fixtures = ['socialapp.json']

    def setUp(self):
        self.path = reverse('users:registration')
        self.data = {
            'first_name': 'Алексей',
            'last_name': 'Баранов',
            'username': 'test001',
            'email': 'test@yandex.ru',
            'password1': '12345678zZ',
            'password2': '12345678zZ',
        }

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], "Регистрация")
        self.assertTemplateUsed(response, template_name='users/registration.html')

    def test_user_registration_post_success(self):
        username = self.data['username']
        self.assertFalse(models.User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)

        # Проверка созданного пользователя
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(models.User.objects.filter(username=username).exists())

    def test_user_registration_post_error(self):
        models.User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Пользователь с таким именем уже существует.", html=True)
