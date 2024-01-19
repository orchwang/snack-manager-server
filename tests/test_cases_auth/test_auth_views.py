import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from snack.core.constants import MemberType


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


class TestUserProfileView:
    @pytest.mark.django_db
    def test_user_profile_response_valid_user_profile_data(self, member_user_1):
        client = APIClient()
        client.force_authenticate(member_user_1)

        response = client.get('/auth/user/profile/')
        assert response.status_code == 200

        response_json = response.json()
        assert response_json['username'] == member_user_1.username
        assert response_json['email'] == member_user_1.email
        assert response_json['member_type'] == member_user_1.member_type

    @pytest.mark.django_db
    def test_user_profile_without_authentication_response_401(self, member_user_1):
        client = APIClient()

        response = client.get('/auth/user/profile/')
        assert response.status_code == 401


class TestUserListView:
    @pytest.mark.django_db
    def test_user_list_view_response_valid_user_list(self, member_user_1, member_user_2, member_user_3, member_user_4):
        client = APIClient()
        client.force_authenticate(member_user_1)

        response = client.get('/auth/users/')
        assert response.status_code == 200

        response_json = response.json()
        users_list = [member_user_1, member_user_2, member_user_3, member_user_4]
        assert len(response_json) == len(users_list)
        for i in range(len(response_json)):
            assert response_json[i]['username'] == users_list[i].username
            assert response_json[i]['email'] == users_list[i].email
            assert response_json[i]['member_type'] == users_list[i].member_type


class TestUpdateUserView:
    @pytest.mark.django_db
    def test_user_list_view_response_valid_user_list(self, member_user_1, member_user_2):
        client = APIClient()
        client.force_authenticate(member_user_1)

        assert member_user_2.member_type == MemberType.MEMBER

        payload = {'member_type': MemberType.ADMIN}
        response = client.put(f'/auth/users/{member_user_2.id}/', payload, format='json')
        assert response.status_code == 200

        response_json = response.json()
        assert response_json['member_type'] == MemberType.ADMIN

        User = get_user_model()
        updated_user = User.objects.get(id=member_user_2.id)
        assert updated_user.member_type == MemberType.ADMIN


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


class TestUserResignView:
    @pytest.mark.django_db
    def test_user_resign_success(self, member_user_1, member_user_2):
        client = APIClient()
        client.force_authenticate(member_user_2)

        response = client.delete('/auth/user/resign/')
        assert response.status_code == 200

        User = get_user_model()
        user = User.objects.get(email=member_user_2.email)

        assert user.is_deleted
        assert not user.is_active

    @pytest.mark.django_db
    def test_last_admin_resign_failed_with_status_400(self, member_user_1, member_user_2):
        client = APIClient()
        client.force_authenticate(member_user_1)

        response = client.delete('/auth/user/resign/')
        assert response.status_code == 400
