import pytest
from rest_framework.test import APIClient


class TestPermissionIsAdmin:
    @pytest.mark.django_db
    def test_is_admin_permission_check_success_with_admin_user(self, member_user_1):
        client = APIClient()
        client.force_authenticate(member_user_1)

        response = client.get('/checks/is_admin/')
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_is_admin_permissoin_check_fail_with_not_admin_user(self, member_user_2):
        client = APIClient()
        client.force_authenticate(member_user_2)

        response = client.get('/checks/is_admin/')
        assert response.status_code == 403
