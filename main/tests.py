from django.test import TestCase
from django.urls import reverse

from main import models


class IndexTestCase(TestCase):
    def test_index(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)


class UserCreateTestCase(TestCase):
    def test_user_creation(self):
        data = {
            "username": "john",
            "password1": "abcdef123456",
            "password2": "abcdef123456",
        }
        response = self.client.post(reverse("user_create"), data)
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
        response_login = self.client.post(reverse("login"), data)
        self.assertEqual(response_login.status_code, 302)

        response_index = self.client.get(reverse("index"))
        user = response_index.context.get("user")
        self.assertTrue(user.is_authenticated)

    def test_login_invalid(self):
        data = {
            "username": "john",
            "password": "wrong_password",
        }
        response_login = self.client.post(reverse("login"), data)
        self.assertEqual(response_login.status_code, 200)

        response_index = self.client.get(reverse("index"))
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
        self.client.post(reverse("login"), data)

    def test_logout(self):
        response_logout = self.client.get(reverse("logout"))
        self.assertEqual(response_logout.status_code, 200)

        response_index = self.client.get(reverse("index"))
        user = response_index.context.get("user")
        self.assertFalse(user.is_authenticated)


class UserDetailTestCase(TestCase):
    def setUp(self):
        user = models.User.objects.create(username="john")
        user.set_password("abcdef123456")
        user.save()
        data = {
            "username": "john",
            "password": "abcdef123456",
        }
        self.client.post(reverse("login"), data)
        self.user = models.User.objects.get(username=data["username"])

    def test_profile(self):
        response = self.client.get(reverse("user_detail", args=(self.user.id,)))
        self.assertEqual(response.status_code, 200)


class UserUpdateTestCase(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(username="john")
        self.user.set_password("abcdef123456")
        self.user.save()

    def test_user_update(self):
        data = {"username": "john2", "email": "john2@example.com"}
        response = self.client.post(reverse("user_update", args=(self.user.id,)), data)
        self.assertEqual(response.status_code, 302)
        updated_user = models.User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.username, data["username"])
        self.assertEqual(updated_user.email, data["email"])


class UserPasswordChangeTestCase(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(username="john")
        self.user.set_password("abcdef123456")
        self.user.save()

    def test_user_password_change(self):
        data = {"username": "john2", "email": "john2@example.com"}
        response = self.client.post(reverse("user_update", args=(self.user.id,)), data)
        self.assertEqual(response.status_code, 302)
        updated_user = models.User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.username, data["username"])
        self.assertEqual(updated_user.email, data["email"])


class UserDeleteTestCase(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(username="john")
        self.user.set_password("abcdef123456")
        self.user.save()

    def test_user_delete(self):
        response = self.client.post(reverse("user_delete", args=(self.user.id,)))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(models.User.objects.filter(id=self.user.id).exists())


class DocumentCreateTestCase(TestCase):
    def test_document_create(self):
        data = {
            "title": "Doc",
            "body": "Content sentence.",
        }
        response = self.client.post(reverse("document_create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(models.Document.objects.get(title=data["title"]))


class DocumentDetailTestCase(TestCase):
    def setUp(self):
        self.data = {
            "title": "Doc",
            "body": "Content sentence.",
        }
        self.client.post(reverse("document_create"), self.data)
        self.doc = models.Document.objects.get(title=self.data["title"])

    def test_document_detail(self):
        response = self.client.get(reverse("document_detail", args=(self.doc.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.data["title"])
        self.assertContains(response, self.data["body"])


class DocumentUpdateTestCase(TestCase):
    def setUp(self):
        data = {
            "title": "Doc",
            "body": "Content sentence.",
        }
        self.client.post(reverse("document_create"), data)
        self.doc = models.Document.objects.get(title=data["title"])

    def test_document_update(self):
        new_data = {
            "title": "New Doc",
            "body": "Brand new content sentence.",
        }
        self.client.post(reverse("document_update", args=(self.doc.id,)), new_data)

        updated_doc = models.Document.objects.get(id=self.doc.id)
        self.assertTrue(updated_doc.title, new_data["title"])
        self.assertTrue(updated_doc.body, new_data["body"])


class DocumentDeleteTestCase(TestCase):
    def setUp(self):
        self.doc = models.Document.objects.create(
            title="Doc", body="Content sentence.",
        )

    def test_document_delete(self):
        self.client.post(reverse("document_delete", args=(self.doc.id,)))
        self.assertFalse(models.Document.objects.all().exists())


class DocumentPurgeTestCase(TestCase):
    def setUp(self):
        # create user
        user = models.User.objects.create(username="john")
        user.set_password("abcdef123456")
        user.save()

        # login user
        data = {
            "username": "john",
            "password": "abcdef123456",
        }
        self.client.post(reverse("login"), data)

        # create user's documents
        models.Document.objects.create(
            title="Doc 1", body="Content sentence 1.", owner=user
        )
        models.Document.objects.create(
            title="Doc 2", body="Content sentence 2.", owner=user
        )
        models.Document.objects.create(
            title="Doc 3", body="Content sentence 3.", owner=user
        )

    def test_document_purge(self):
        response = self.client.post(reverse("document_purge"))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(models.Document.objects.all().exists())


class DocumentPurgeAnonymousTestCase(TestCase):
    def setUp(self):
        # create user
        user = models.User.objects.create(username="john")

        # create user's documents
        models.Document.objects.create(
            title="Doc 1", body="Content sentence 1.", owner=user
        )
        models.Document.objects.create(
            title="Doc 2", body="Content sentence 2.", owner=user
        )
        models.Document.objects.create(
            title="Doc 3", body="Content sentence 3.", owner=user
        )

    def test_document_purge(self):
        response = self.client.post(reverse("document_purge"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue("login" in response.url)
        self.assertEqual(models.Document.objects.all().count(), 3)


class DocumentImportTestCase(TestCase):
    def setUp(self):
        # create user
        user = models.User.objects.create(username="john")
        user.set_password("abcdef123456")
        user.save()

        # login user
        data = {
            "username": "john",
            "password": "abcdef123456",
        }
        self.client.post(reverse("login"), data)

    def test_document_import(self):
        filename = "README.md"
        with open(filename) as fp:
            self.client.post(reverse("document_import"), {"file": fp})
            self.assertEqual(
                models.Document.objects.get(title=filename).title, filename
            )
