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


class TestTokenAuthViews:
    @pytest.mark.django_db
    def test_with_username_and_password_get_token_success(self, member_user_1):
        client = APIClient()

        payload = {'username': member_user_1.username, 'password': 'password'}

        response = client.post('/auth/token/', data=payload)
        assert response.status_code == 200

        response_json = response.json()
        assert response_json['access']
        assert response_json['refresh']

    @pytest.mark.django_db
    def test_with_invalid_username_response_401(self, member_user_1):
        client = APIClient()

        payload = {'username': 'fakeusername', 'password': 'password'}

        response = client.post('/auth/token/', data=payload)
        assert response.status_code == 401

        response_json = response.json()
        assert response_json['detail'] == 'No active account found with the given credentials'

    @pytest.mark.django_db
    def test_with_invalid_password_response_401(self, member_user_1):
        client = APIClient()

        payload = {'username': member_user_1.username, 'password': 'fakepassword'}

        response = client.post('/auth/token/', data=payload)
        assert response.status_code == 401

        response_json = response.json()
        assert response_json['detail'] == 'No active account found with the given credentials'

    @pytest.mark.django_db
    def test_with_access_token_authentication_success(self, dummy_orders_set_1, member_user_1):
        client = APIClient()

        payload = {'username': member_user_1.username, 'password': 'password'}

        response = client.post('/auth/token/', data=payload)
        assert response.status_code == 200

        response_json = response.json()
        assert response_json['access']
        assert response_json['refresh']

        access_token = response_json['access']

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

        response = client.get('/checks/is_authenticated/')
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_with_invalid_access_token_authentication_success(self, dummy_orders_set_1, member_user_1):
        client = APIClient()

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'fakeaccesstoken')

        response = client.get('/checks/is_authenticated/')
        assert response.status_code == 401
