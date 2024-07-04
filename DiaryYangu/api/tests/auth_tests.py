from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from api.models.auth_models import UserProfile
import json

class AuthViewsTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'password': 'password123',
            'email': 'testuser@example.com'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.user_profile = UserProfile.objects.create(user=self.user, bio='Initial bio', is_active=True)

    def test_user_creation_and_profile_creation(self):
        response = self.client.post(reverse('user-create'), {
            'username': 'newuser',
            'password': 'password123',
            'email': 'newuser@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_id = response.data['user']['id']
        user_profile = UserProfile.objects.get(user__id=user_id)
        self.assertIsNotNone(user_profile)
        self.assertEqual(user_profile.user.username, 'newuser')

    def test_retrieve_user_profile(self):
        url = reverse('user-profile-detail', kwargs={'user_id': self.user.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bio'], 'Initial bio')

    def test_update_user_profile(self):
        url = reverse('user-profile-detail', kwargs={'user_id': self.user.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, {'bio': 'Updated bio'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user_profile.refresh_from_db()
        self.assertEqual(self.user_profile.bio, 'Updated bio')

    def test_deactivate_user_profile(self):
        url = reverse('user-profile-deactivate', kwargs={'user_id': self.user.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user_profile.refresh_from_db()
        self.assertFalse(self.user_profile.is_active)

    def test_password_reset_request(self):
        url = reverse('password-reset')
        response = self.client.post(url, {'email': self.user.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_password_reset_confirm(self):
        reset_url = reverse('password-reset')
        response = self.client.post(reset_url, {'email': self.user.email})
        token = response.data['token']

        confirm_url = reverse('password-reset-confirm')
        new_password = 'newpassword123'
        response = self.client.post(confirm_url, {'token': token, 'new_password': new_password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that the password was updated
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))
