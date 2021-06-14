from django.test import TestCase, Client
from django.urls import reverse
from main.models import UserProfiles
from django.contrib.auth.models import User, auth


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.profile_url = reverse('profile')
        self.main_url = reverse('home')

        self.user = User.objects.create_user(username="testuser")
        self.user.set_password('123456')
        self.user.save()
        self.client.login(username='testuser', password="123456")

    def test_main_GET(self):
        response = self.client.get(self.main_url)

        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, "home.html")

    def test_new_userprofile_GET(self):
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")

    def test_existing_userprofile_GET(self):
        userProfile = UserProfiles()
        userProfile.user = self.user
        userProfile.topics = "Java,Android"
        userProfile.save()

        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")

    def test_userprofile_POST(self):
        response = self.client.post(self.profile_url, {
            "topics": "Java,Android"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(UserProfiles.objects.get(user=self.user).topics, "Java,Android")
