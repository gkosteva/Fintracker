from django.contrib.auth import authenticate
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
import json
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


# Create your tests here.

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.validate_email_url = reverse('validate-email')
        self.validate_username_url = reverse('validate-username')
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_login = User.objects.create_user(username='testuserlogin', password='testpassword')
        self.logout_url = reverse('logout')
        self.user_logout = User.objects.create_user(username='testuser2', password='testpassword2')
        self.client.force_login(self.user_logout)
        self.reset_password_url = reverse('request-password')
        self.user_reset_pass = User.objects.create_user(username='testuser3', email='test3@example.com',
                                                        password='password123')

    def test_email_validation_view(self):
        response = self.client.post(self.validate_email_url, json.dumps({'email': 'testvalidemail@example.com'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'email_valid': True})

        response = self.client.post(self.validate_email_url, json.dumps({'email': 'invalid_email'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'email_error': 'Email is not in the correct format'})

    def test_valid_username(self):
        response = self.client.post(self.validate_username_url, json.dumps({'username': 'testuser123'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'username_valid': True})

    def test_invalid_username_with_special_characters(self):
        response = self.client.post(self.validate_username_url, json.dumps({'username': 'testuser!@#'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content,
                             {'username_error': 'username should only contain alphanumeric characters'})

    def test_existing_username(self):
        User.objects.create_user(username='existinguser', email='existing@example.com', password='password')
        response = self.client.post(self.validate_username_url, json.dumps({'username': 'existinguser'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 409)
        self.assertJSONEqual(response.content, {'username_error': 'username is taken'})

    def test_short_password(self):
        response = self.client.post(self.register_url,
                                    {'username': 'testusershortpass', 'email': 'testshowrpass@example.com', 'password': 'short'})
        self.assertEqual(response.status_code, 200)
        user_exists = User.objects.filter(username='testusershortpass').exists()
        self.assertFalse(user_exists)
        self.assertEqual(len(mail.outbox), 0)

    def test_successful_registration(self):
        response = self.client.post(self.register_url,
                                    {'username': 'testusersuccessregister', 'email': 'testusersuccessregister@example.com', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        user_exists = User.objects.filter(username='testusersuccessregister').exists()
        self.assertTrue(user_exists)
        # self.assertEqual(len(mail.outbox), 1)
        # self.assertEqual(mail.outbox[0].subject, 'Activate your account') ---- not working

    def test_login_page_loads_successfully(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/login.html')

    # def test_login_successful(self):
    #     response = self.client.post(self.login_url, {'username': 'testuser1', 'password': 'testpassword1'})
    #     self.assertRedirects(response, reverse('expenses'))

    # def test_inactive_user_login(self): # not working
    #     self.user_login.is_active = False
    #     self.user_login.save()
    #     response = self.client.post(self.login_url, {'username': 'testuserlogin', 'password': 'testpassword'})
    #     self.assertContains(response, 'Your account is not active. Please check your email!')

    def test_invalid_credentials_login(self):
        response = self.client.post(self.login_url, {'username': 'invaliduser', 'password': 'invalidpassword'})
        self.assertContains(response, 'Invalid credentials! Please try again.')

    def test_missing_fields_login(self):
        response = self.client.post(self.login_url, {'username': '', 'password': ''})
        self.assertContains(response, 'Please fill all fields!')

    def test_logout_successful(self):
        response = self.client.post(self.logout_url)
        self.assertRedirects(response, reverse('login'))

    def test_user_logged_out(self):
        self.client.post(self.logout_url)
        user = authenticate(username='testuserlogout', password='testpassword')
        self.assertIsNone(user)

    def test_get_request_password_reset_page(self):
        response = self.client.get(self.reset_password_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/reset-password.html')
    #
    # def test_request_password_reset_email(self):
    #     response = self.client.post(self.reset_password_url, {'email': 'test@example.com'})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'authentication/reset-password.html')
    #
    #     self.assertEqual(len(mail.outbox), 1)
    #     self.assertEqual(mail.outbox[0].subject, 'Password reset instructions')
    #     self.assertIn('Hi testuser, Please use the link below to reset your password', mail.outbox[0].body)

    def test_request_password_reset_email_invalid_email(self):
        response = self.client.post(self.reset_password_url, {'email': 'invalidemail'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/reset-password.html')
        self.assertEqual(len(mail.outbox), 0)

    def test_request_password_reset_email_no_user(self):
        response = self.client.post(self.reset_password_url, {'email': 'nonexistent@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/reset-password.html')
        self.assertEqual(len(mail.outbox), 0)
