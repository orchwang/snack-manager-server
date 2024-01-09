import pytest
from rest_framework.test import APIClient


class TestGetCartListView:
    @pytest.mark.django_db
    def test_get_order_list_response_status_200(self, dummy_orders_set_1, member_user_1):
        client = APIClient()
        client.force_authenticate(member_user_1)

        response = client.get('/orders/')
        assert response.status_code == 200
        assert len(response.json()) == len(dummy_orders_set_1)


class TestRetrieveCartView:
    @pytest.mark.django_db
    def test_retrieve_order_response_status_200(self, dummy_orders_set_1, member_user_1):
        client = APIClient()
        client.force_authenticate(member_user_1)

        response = client.get(f'/order/{dummy_orders_set_1[0].uid}/')
        assert response.status_code == 200

        response_json = response.json()
        assert response_json['uid'] == dummy_orders_set_1[0].uid
        assert response_json['user'] == dummy_orders_set_1[0].user.id


class TestGetSnackListView:
    @pytest.mark.django_db
    def test_get_snack_list_response_status_200(self, dummy_orders_set_1, member_user_1):
        client = APIClient()
        client.force_authenticate(member_user_1)

        response = client.get('/snacks/')
        assert response.status_code == 200
