from django.test import TestCase, Client
from django.urls import reverse
from main.models import UserProfiles
from django.contrib.auth.models import User, auth


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

        self.user = User.objects.create_user(username="testuser", email="testuser@email.com")
        self.user.set_password('123456')
        self.user.save()
        self.client.login(username='testuser', password="123456")

    def test_register_GET(self):
        response = self.client.get(self.register_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_valid_register_POST(self):
        response = self.client.post(self.register_url, {
            "first_name": "user",
            "last_name": "1",
            "username": "user1",
            "email": "user1@email.com",
            "password1": "123456",
            "password2": "123456"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.get(username="user1").first_name, "user")

    def test_invalid_register_password_mismatch_POST(self):
        response = self.client.post(self.register_url, {
            "first_name": "user",
            "last_name": "1",
            "username": "user1",
            "email": "user1@email.com",
            "password1": "123456",
            "password2": "12345"
        })

        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username="user1").exists())

    def test_invalid_register_username_exists_POST(self):
        response = self.client.post(self.register_url, {
            "first_name": "user",
            "last_name": "1",
            "username": "testuser",
            "email": "user1@email.com",
            "password1": "123456",
            "password2": "12345"
        })

        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username="user1").exists())

    def test_invalid_register_email_exists_POST(self):
        response = self.client.post(self.register_url, {
            "first_name": "user",
            "last_name": "1",
            "username": "user1",
            "email": "testuser@email.com",
            "password1": "123456",
            "password2": "12345"
        })

        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username="user1").exists())

    def test_login_GET(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_valid_login_POST(self):
        self.client.logout()
        t_user = User.objects.create_user(username="testuser2", email="testuser2@email.com")
        t_user.set_password('123456')
        t_user.save()

        response = self.client.post(self.login_url, {
            "username": "testuser2",
            "password": "123456"
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="testuser2").exists())
        self.assertEqual(int(self.client.session['_auth_user_id']), t_user.pk)

    def test_invalid_login_POST(self):
        self.client.logout()
        t_user = User.objects.create_user(username="testuser2", email="testuser2@email.com")
        t_user.set_password('123456')
        t_user.save()

        response = self.client.post(self.login_url, {
            "username": "testuser2",
            "password": "12345"
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="testuser2").exists())
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_logout_GET(self):
        self.assertIn('_auth_user_id', self.client.session)

        response = self.client.post(self.logout_url)

        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEqual(response.status_code, 302)



