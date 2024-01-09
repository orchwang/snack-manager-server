import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


class TestUserSignUpView:
    @pytest.mark.django_db
    def test_user_sign_up_success(self):
        client = APIClient()

        payload = {'username': 'test_user', 'password': 'password', 'email': 'test_user@test.com'}

        response = client.post('/auth/sign-up/', data=payload)
        assert response.status_code == 201

        User = get_user_model()
        user = User.objects.get(email=payload['email'])

        assert user.username == payload['username']
        assert user.email == payload['email']

    @pytest.mark.django_db
    def test_user_sign_up_with_duplicated_email_failed(self, member_user_1):
        client = APIClient()

        payload = {'username': 'test_username', 'password': 'password', 'email': member_user_1.email}

        response = client.post('/auth/sign-up/', data=payload)
        assert response.status_code == 400
