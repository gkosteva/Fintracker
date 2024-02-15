from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserPreferences


class TestViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_index_GET(self):
        response = self.client.get(reverse('preferences'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'preference/index.html')

    def test_index_POST_exists(self):
        UserPreferences.objects.create(user=self.user, currency='USD')
        response = self.client.post(reverse('preferences'), {'currency': 'EUR'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Changes saved!")
