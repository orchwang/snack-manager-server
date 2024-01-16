import json

import pytest

from rest_framework.test import APIClient

from django.conf import settings
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

from snack.order.models import Purchase


class TestGetOrderListView:
    @pytest.mark.django_db
    def test_get_order_list_response_status_200(self, dummy_orders_set_1, member_user_1):
        client = APIClient()
        client.force_authenticate(member_user_1)

        response = client.get('/orders/')
        assert response.status_code == 200
        assert len(response.json()) == len(dummy_orders_set_1)


class TestRetrieveOrderView:
    @pytest.mark.django_db
    def test_retrieve_order_response_status_200(self, dummy_orders_set_1, member_user_1):
        client = APIClient()
        client.force_authenticate(member_user_1)

        response = client.get(f'/orders/{dummy_orders_set_1[0].uid}/')
        assert response.status_code == 200

        response_json = response.json()
        assert response_json['uid'] == dummy_orders_set_1[0].uid
        assert response_json['user_id'] == dummy_orders_set_1[0].user.id
        assert response_json['user_email'] == dummy_orders_set_1[0].user.email

        purchases = Purchase.objects.filter(order=dummy_orders_set_1[0].id).all()
        assert len(response_json['purchase_set']) == purchases.count()
        for i in range(len(response_json['purchase_set'])):
            assert purchases[i].snack.id == response_json['purchase_set'][i]['snack']['id']
            assert purchases[i].snack.uid == response_json['purchase_set'][i]['snack']['uid']
            assert purchases[i].snack.name == response_json['purchase_set'][i]['snack']['name']


class TestGetSnackListView:
    @pytest.mark.django_db
    def test_get_snack_list_response_status_200(self, dummy_orders_set_1, dummy_snacks_set_1, member_user_1):
        client = APIClient()
        client.force_authenticate(member_user_1)

        response = client.get('/snacks/')
        assert response.status_code == 200

        response_json = response.json()
        for i in range(len(response_json)):
            assert response_json[i]['uid'] == dummy_snacks_set_1[i].uid
            assert response_json[i]['name'] == dummy_snacks_set_1[i].name


class TestRetrieveSnackView:
    @pytest.mark.django_db
    def test_retrieve_snack_detail_response_status_200(self, dummy_orders_set_1, dummy_snacks_set_1, member_user_1):
        client = APIClient()
        client.force_authenticate(member_user_1)

        response = client.get(f'/snacks/{dummy_snacks_set_1[0].uid}/')
        assert response.status_code == 200

        response_json = response.json()
        assert response_json['uid'] == dummy_snacks_set_1[0].uid
        assert response_json['name'] == dummy_snacks_set_1[0].name


class TestPostSnackView:
    @pytest.mark.django_db
    def test_create_snack_response_status_201(self, member_user_1):
        client = APIClient()
        client.force_authenticate(member_user_1)

        snacks_json_path = f'{settings.TEST_DIR}/fixtures/snacks_raw_data/snacks.json'
        with open(snacks_json_path, 'r') as json_file:
            snacks_data = json.load(json_file)

        image = File(
            open(
                f'{settings.TEST_DIR}/fixtures/snacks_raw_data/{snacks_data[0].get("image")}',
                'rb',
            )
        )
        upload_image = SimpleUploadedFile(
            f'{snacks_data[0].get("image")}', image.read(), content_type='multipart/form-data'
        )
        payload = {
            'name': snacks_data[0].get('name'),
            'url': snacks_data[0].get('url'),
            'image': upload_image,
            'desc': snacks_data[0].get('desc'),
            'price': snacks_data[0].get('price'),
            'currency': snacks_data[0].get('currency'),
        }

        response = client.post('/snacks/', payload, format='multipart')
        assert response.status_code == 201

        response_json = response.json()
        assert response_json
