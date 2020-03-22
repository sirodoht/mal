from django.test import TestCase
from django.urls import reverse

from main import models


class SignupTestCase(TestCase):
    def test_user_creation(self):
        data = {
            "username": "john",
            "password1": "abcdef123456",
            "password2": "abcdef123456",
        }
        response = self.client.post(reverse("main:signup"), data)
        self.assertEquals(response.status_code, 302)
        self.assertTrue(models.User.objects.get(username=data["username"]))


class LoginTestCase(TestCase):
    def setUp(self):
        user = models.User.objects.create(username="john")
        user.set_password("abcdef123456")
        user.save()

    def test_login(self):
        data = {
            "username": "john",
            "password": "abcdef123456",
        }
        response_login = self.client.post(reverse("main:login"), data)
        self.assertEquals(response_login.status_code, 302)

        response_index = self.client.get(reverse("main:index"))
        user = response_index.context.get("user")
        self.assertTrue(user.is_authenticated)

    def test_login_invalid(self):
        data = {
            "username": "john",
            "password": "wrong_password",
        }
        response_login = self.client.post(reverse("main:login"), data)
        self.assertEquals(response_login.status_code, 200)

        response_index = self.client.get(reverse("main:index"))
        self.assertEquals(response_index.status_code, 200)

        user = response_index.context.get("user")
        self.assertFalse(user.is_authenticated)


class LogoutTestCase(TestCase):
    def setUp(self):
        user = models.User.objects.create(username="john")
        user.set_password("abcdef123456")
        user.save()
        data = {
            "username": "john",
            "password": "abcdef123456",
        }
        self.client.post(reverse("main:login"), data)

    def test_logout(self):
        response_logout = self.client.get(reverse("main:logout"))
        self.assertEquals(response_logout.status_code, 200)

        response_index = self.client.get(reverse("main:index"))
        user = response_index.context.get("user")
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def setUp(self):
        user = models.User.objects.create(username="john")
        user.set_password("abcdef123456")
        user.save()
        data = {
            "username": "john",
            "password": "abcdef123456",
        }
        self.client.post(reverse("main:login"), data)

    def test_profile(self):
        response = self.client.post(reverse("main:profile"))
        self.assertEquals(response.status_code, 200)
