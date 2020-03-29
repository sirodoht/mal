from django.test import TestCase
from django.urls import reverse

from main import models


class IndexTestCase(TestCase):
    def test_index(self):
        response = self.client.get(reverse("main:index"))
        self.assertEqual(response.status_code, 200)


class SignupTestCase(TestCase):
    def test_user_creation(self):
        data = {
            "username": "john",
            "password1": "abcdef123456",
            "password2": "abcdef123456",
        }
        response = self.client.post(reverse("main:signup"), data)
        self.assertEqual(response.status_code, 302)
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
        self.assertEqual(response_login.status_code, 302)

        response_index = self.client.get(reverse("main:index"))
        user = response_index.context.get("user")
        self.assertTrue(user.is_authenticated)

    def test_login_invalid(self):
        data = {
            "username": "john",
            "password": "wrong_password",
        }
        response_login = self.client.post(reverse("main:login"), data)
        self.assertEqual(response_login.status_code, 200)

        response_index = self.client.get(reverse("main:index"))
        self.assertEqual(response_index.status_code, 200)

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
        self.assertEqual(response_logout.status_code, 200)

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
        self.assertEqual(response.status_code, 200)


class ProfileLoggedOutTestCase(TestCase):
    def test_profile_noauth(self):
        response = self.client.post(reverse("main:profile"))
        self.assertEqual(response.status_code, 302)


class DocumentCreateTestCase(TestCase):
    def test_document_create(self):
        data = {
            "title": "Doc",
            "body": "Content sentence.",
        }
        response = self.client.post(reverse("main:document_create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(models.Document.objects.get(title=data["title"]))


class DocumentDetailTestCase(TestCase):
    def setUp(self):
        self.data = {
            "title": "Doc",
            "body": "Content sentence.",
        }
        self.client.post(reverse("main:document_create"), self.data)
        self.doc = models.Document.objects.get(title=self.data["title"])

    def test_document_detail(self):
        response = self.client.get(reverse("main:document_detail", args=(self.doc.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.data["title"])
        self.assertContains(response, self.data["body"])


class DocumentUpdateTestCase(TestCase):
    def setUp(self):
        data = {
            "title": "Doc",
            "body": "Content sentence.",
        }
        self.client.post(reverse("main:document_create"), data)
        self.doc = models.Document.objects.get(title=data["title"])

    def test_document_update(self):
        new_data = {
            "title": "New Doc",
            "body": "Brand new content sentence.",
        }
        self.client.post(reverse("main:document_update", args=(self.doc.id,)), new_data)

        updated_doc = models.Document.objects.get(id=self.doc.id)
        self.assertTrue(updated_doc.title, new_data["title"])
        self.assertTrue(updated_doc.body, new_data["body"])


class DocumentDeleteTestCase(TestCase):
    def setUp(self):
        data = {
            "title": "Doc",
            "body": "Content sentence.",
        }
        self.client.post(reverse("main:document_create"), data)
        self.doc = models.Document.objects.get(title=data["title"])

    def test_document_delete(self):
        self.client.post(reverse("main:document_delete", args=(self.doc.id,)))
        self.assertFalse(models.Document.objects.all().exists())
