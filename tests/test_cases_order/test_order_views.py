import json
import random
from datetime import timedelta

import pytest
from django.utils import timezone

from rest_framework.test import APIClient

from django.conf import settings
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

from snack.order.constants import SnackReactionType, OrderStatus
from snack.order.models import Purchase, Order, Snack, SnackReaction


class TestGetOrderListView:
    @pytest.mark.django_db
    def test_get_order_list_response_status_200(self, dummy_orders_set_1, member_user_1):
        client = APIClient()
        client.force_authenticate(member_user_1)

        response = client.get('/orders/')
        assert response.status_code == 200
        assert len(response.json()) == len(dummy_orders_set_1)

    @pytest.mark.django_db
    def test_get_order_list_response_with_uid_fileter_response_specific_order(self, dummy_orders_set_1, member_user_1):
        client = APIClient()
        client.force_authenticate(member_user_1)

        response = client.get(f'/orders/?uid={dummy_orders_set_1[0].uid}')
        assert response.status_code == 200
        assert len(response.json()) == 1
        response_json = response.json()
        assert response_json[0]['uid'] == dummy_orders_set_1[0].uid

    @pytest.mark.django_db
    def test_get_order_list_response_with_status_fileter_response_specific_order(
        self, dummy_orders_set_1, member_user_1
    ):
        client = APIClient()
        client.force_authenticate(member_user_1)

        ordered_order = dummy_orders_set_1[1]
        ordered_order.status = OrderStatus.ORDERED
        ordered_order.save()

        ordered_orders = Order.objects.filter(status=OrderStatus.ORDERED).all()
        assert ordered_orders.count() == 1

        response = client.get(f'/orders/?status={OrderStatus.ORDERED.value}')
        assert response.status_code == 200
        response_json = response.json()
        assert response_json[0]['uid'] == dummy_orders_set_1[1].uid

    @pytest.mark.django_db
    def test_get_order_list_response_with_ordering_query_param_response_sorted_response(
        self, dummy_orders_set_1, member_user_1
    ):
        client = APIClient()
        client.force_authenticate(member_user_1)

        response = client.get('/orders/?ordering=created_at')
        assert response.status_code == 200
        response_json = response.json()
        assert response_json[0]['uid'] == dummy_orders_set_1[0].uid

        response = client.get('/orders/?ordering=-created_at')
        assert response.status_code == 200
        response_json = response.json()
        assert response_json[0]['uid'] == dummy_orders_set_1[4].uid

    @pytest.mark.django_db
    def test_get_order_list_response_with_created_at_get_response_200(self, dummy_orders_set_1, member_user_1):
        client = APIClient()
        client.force_authenticate(member_user_1)

        seven_days_after = timezone.now() + timedelta(days=7)
        iso_format_date = seven_days_after.strftime('%Y-%m-%dT%H:%M:%S')

        response = client.get(f'/orders/?created_at__gte={iso_format_date}')
        assert response.status_code == 200

        response_json = response.json()
        assert not response_json

    @pytest.mark.django_db
    def test_get_order_list_with_year_filter_response_200(self, dummy_orders_set_1, member_user_1):
        client = APIClient()
        client.force_authenticate(member_user_1)

        response = client.get(f'/orders/?year={dummy_orders_set_1[0].created_at.year}')
        assert response.status_code == 200

        orders = Order.objects.filter(year=dummy_orders_set_1[0].created_at.year).all()

        response_json = response.json()
        assert len(response_json) == orders.count()

    @pytest.mark.django_db
    def test_get_order_list_with_month_filter_response_200(self, dummy_orders_set_1, member_user_1):
        different_month_date = timezone.now() - timedelta(days=300)

        order_2 = dummy_orders_set_1[1]
        order_2.created_at = different_month_date
        order_2.year = different_month_date.year
        order_2.month = different_month_date.month
        order_2.day = different_month_date.day
        order_2.save()

        order_3 = dummy_orders_set_1[2]
        order_3.created_at = different_month_date
        order_3.year = different_month_date.year
        order_3.month = different_month_date.month
        order_3.day = different_month_date.day
        order_3.save()

        client = APIClient()
        client.force_authenticate(member_user_1)

        response = client.get(f'/orders/?month={dummy_orders_set_1[0].created_at.month}')
        assert response.status_code == 200

        orders = Order.objects.filter(month=dummy_orders_set_1[0].created_at.month).all()

        response_json = response.json()
        assert len(response_json) == 3
        assert len(response_json) == orders.count()


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

    @pytest.mark.django_db
    def test_retrieve_order_response_status_400(self, dummy_orders_set_1, member_user_1):
        client = APIClient()
        client.force_authenticate(member_user_1)

        response = client.get('/orders/fakeuid/')
        assert response.status_code == 404


class TestPostOrderView:
    @pytest.mark.django_db
    def test_create_order_response_status_201(
        self, member_user_1, dummy_orders_set_1, dummy_snacks_set_1, dummy_snacks_reaction_set_1
    ):
        # Make all orders are delivered or cancelled
        order_1 = dummy_orders_set_1[0]
        order_2 = dummy_orders_set_1[1]
        order_3 = dummy_orders_set_1[2]
        order_4 = dummy_orders_set_1[3]
        order_5 = dummy_orders_set_1[4]

        order_1.status = OrderStatus.CANCELLED
        order_2.status = OrderStatus.COMPLETED
        order_3.status = OrderStatus.COMPLETED
        order_4.status = OrderStatus.COMPLETED
        order_5.status = OrderStatus.CANCELLED

        order_1.save()
        order_2.save()
        order_3.save()
        order_4.save()
        order_5.save()

        client = APIClient()
        client.force_authenticate(member_user_1)

        snacks = []
        snacks_to_order = [
            dummy_snacks_set_1[0],
            dummy_snacks_set_1[1],
            dummy_snacks_set_1[3],
            dummy_snacks_set_1[4],
        ]

        for snack in snacks_to_order:
            snacks.append({'uid': snack.uid, 'quantity': random.randrange(1, 40)})

        payload = {
            'snacks': snacks,
        }

        response = client.post('/orders/', payload, format='json')
        assert response.status_code == 201

        response_json = response.json()
        assert response_json

        created_order = Order.objects.get(uid=response_json['uid'])
        assert created_order.uid == response_json['uid']
        for item in snacks:
            snack = Snack.objects.get(uid=item['uid'])
            created_purchases = Purchase.objects.filter(order=created_order, snack=snack).get()
            assert created_purchases.quantity == item['quantity']

    @pytest.mark.django_db
    def test_create_order_with_not_delivered_orders_response_status_400(
        self, member_user_1, dummy_orders_set_1, dummy_snacks_set_1
    ):
        # Make all orders are delivered or cancelled
        order_1 = dummy_orders_set_1[0]
        order_2 = dummy_orders_set_1[1]

        order_1.status = OrderStatus.CREATED
        order_2.status = OrderStatus.SHIPPING

        order_1.save()
        order_2.save()

        client = APIClient()
        client.force_authenticate(member_user_1)

        snacks = []
        for snack in [dummy_snacks_set_1[0], dummy_snacks_set_1[1], dummy_snacks_set_1[3]]:
            snacks.append({'uid': snack.uid, 'quantity': random.randrange(1, 40)})
        payload = {
            'snacks': snacks,
        }

        response = client.post('/orders/', payload, format='json')
        assert response.status_code == 400

        response_json = response.json()
        assert response_json['detail'] == 'You cannot order when not delivered snack is in your order.'

    @pytest.mark.django_db
    def test_create_order_with_invalid_snack_response_status_400(self, member_user_1, dummy_snacks_set_1):
        client = APIClient()
        client.force_authenticate(member_user_1)

        all_orders_count = Order.objects.count()

        snacks = []
        for snack in dummy_snacks_set_1:
            snacks.append({'uid': snack.uid, 'quantity': random.randrange(1, 40)})
        snacks.append({
            'uid': 'notavailableuid',
            'quantity': 1000,
        })
        payload = {
            'snacks': snacks,
        }

        response = client.post('/orders/', payload, format='json')
        assert response.status_code == 400

        orders_count_after_request = Order.objects.all().count()
        assert all_orders_count == orders_count_after_request

        created_purchase_count = Purchase.objects.all().count()
        assert not created_purchase_count

    @pytest.mark.django_db
    def test_create_order_without_snack_response_status_400(
        self, member_user_1, dummy_orders_set_1, dummy_snacks_set_1
    ):
        client = APIClient()
        client.force_authenticate(member_user_1)

        all_orders_count = Order.objects.count()

        payload = {
            'snacks': [],
        }

        response = client.post('/orders/', payload, format='json')
        assert response.status_code == 400

        orders_count_after_request = Order.objects.count()
        assert all_orders_count == orders_count_after_request

    @pytest.mark.django_db
    def test_create_order_with_wrong_type_snack_response_status_400(
        self, member_user_1, dummy_orders_set_1, dummy_snacks_set_1
    ):
        client = APIClient()
        client.force_authenticate(member_user_1)

        all_orders_count = Order.objects.count()

        payload = {
            'snacks': 'string is not valid payload',
        }

        response = client.post('/orders/', payload, format='json')
        assert response.status_code == 400

        orders_count_after_request = Order.objects.count()
        assert all_orders_count == orders_count_after_request

    @pytest.mark.django_db
    def test_create_order_should_failed_with_snack_which_has_hate_reaction_more_than_like(
        self, member_user_1, dummy_orders_set_1, dummy_snacks_set_1, dummy_snacks_reaction_set_1
    ):
        """
        dummy_snacks_reaction_set_1[2] has more hate reaction than like reaction
        """
        client = APIClient()
        client.force_authenticate(member_user_1)

        snacks = []
        for snack in dummy_snacks_set_1:
            snacks.append({'uid': snack.uid, 'quantity': random.randrange(1, 40)})
        payload = {
            'snacks': snacks,
        }

        response = client.post('/orders/', payload, format='json')
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_create_order_should_create_year_month_day_field_value(
        self, member_user_1, dummy_orders_set_1, dummy_snacks_set_1, dummy_snacks_reaction_set_1
    ):
        # Make all orders are delivered or cancelled
        order_1 = dummy_orders_set_1[0]
        order_2 = dummy_orders_set_1[1]
        order_3 = dummy_orders_set_1[2]
        order_4 = dummy_orders_set_1[3]
        order_5 = dummy_orders_set_1[4]

        order_1.status = OrderStatus.CANCELLED
        order_2.status = OrderStatus.COMPLETED
        order_3.status = OrderStatus.COMPLETED
        order_4.status = OrderStatus.COMPLETED
        order_5.status = OrderStatus.CANCELLED

        order_1.save()
        order_2.save()
        order_3.save()
        order_4.save()
        order_5.save()

        client = APIClient()
        client.force_authenticate(member_user_1)

        snacks = []
        snacks_to_order = [
            dummy_snacks_set_1[0],
            dummy_snacks_set_1[1],
            dummy_snacks_set_1[3],
            dummy_snacks_set_1[4],
        ]

        for snack in snacks_to_order:
            snacks.append({'uid': snack.uid, 'quantity': random.randrange(1, 40)})

        payload = {
            'snacks': snacks,
        }

        response = client.post('/orders/', payload, format='json')
        assert response.status_code == 201

        response_json = response.json()
        assert response_json

        created_order = Order.objects.get(uid=response_json['uid'])
        assert created_order.year == created_order.created_at.year
        assert created_order.month == created_order.created_at.month
        assert created_order.day == created_order.created_at.day


class TestUpdateOrderView:
    @pytest.mark.django_db
    def test_update_order_with_snack_data_response_200(
        self, member_user_1, dummy_orders_set_1, dummy_snacks_set_1, dummy_snacks_reaction_set_1
    ):
        client = APIClient()
        client.force_authenticate(member_user_1)

        existing_order_purchases = Purchase.objects.filter(order=dummy_orders_set_1[0]).all()
        assert len(existing_order_purchases) == 2
        assert existing_order_purchases[0].snack == dummy_snacks_set_1[2]
        assert existing_order_purchases[1].snack == dummy_snacks_set_1[3]

        snacks = []
        for snack in dummy_snacks_set_1:
            snacks.append({'uid': snack.uid, 'quantity': random.randrange(1, 40)})
        payload = {'snacks': snacks}

        response = client.put(f'/orders/{dummy_orders_set_1[0].uid}/', payload, format='json')
        assert response.status_code == 200

        response_json = response.json()
        assert response_json

        created_order = Order.objects.get(uid=response_json['uid'])
        assert created_order.uid == response_json['uid']
        for item in snacks:
            snack = Snack.objects.get(uid=item['uid'])
            created_purchases = Purchase.objects.filter(order=created_order, snack=snack).get()
            assert created_purchases.quantity == item['quantity']


class TestGetSnackListView:
    @pytest.mark.django_db
    def test_get_snack_list_response_status_200(
        self, dummy_orders_set_1, dummy_snacks_set_1, dummy_snacks_reaction_set_1, member_user_1
    ):
        client = APIClient()
        client.force_authenticate(member_user_1)

        response = client.get('/snacks/')
        assert response.status_code == 200

        response_json = response.json()
        for i in range(len(response_json)):
            assert response_json[i]['uid'] == dummy_snacks_set_1[i].uid
            assert response_json[i]['name'] == dummy_snacks_set_1[i].name

    @pytest.mark.django_db
    def test_get_snack_list_with_like_reaction_count_response_valid_list(
        self, dummy_orders_set_1, dummy_snacks_set_1, dummy_snacks_reaction_set_1, member_user_1
    ):
        client = APIClient()
        client.force_authenticate(member_user_1)

        response = client.get('/snacks/?ordering=like_reaction_count,created_at')
        assert response.status_code == 200

        response_json = response.json()
        assert response_json


class TestRetrieveSnackView:
    @pytest.mark.django_db
    def test_retrieve_snack_detail_response_status_200(
        self, dummy_orders_set_1, dummy_snacks_set_1, dummy_snacks_reaction_set_1, member_user_1
    ):
        return
        client = APIClient()
        client.force_authenticate(member_user_1)

        response = client.get(f'/snacks/{dummy_snacks_set_1[0].uid}/')
        assert response.status_code == 200

        response_json = response.json()
        assert response_json['uid'] == dummy_snacks_set_1[0].uid
        assert response_json['name'] == dummy_snacks_set_1[0].name


class TestUpdateOrderStatus:
    @pytest.mark.django_db
    def test_update_order_status_to_approved_success(
        self, dummy_orders_set_1, dummy_snacks_set_1, dummy_snacks_reaction_set_1, member_user_1
    ):
        client = APIClient()
        client.force_authenticate(member_user_1)

        assert dummy_orders_set_1[2].status == OrderStatus.CREATED

        payload = {
            'status': OrderStatus.APPROVED.value,
        }
        response = client.patch(f'/orders/{dummy_orders_set_1[2].uid}/status/', data=payload, format='json')
        assert response.status_code == 200

        response_json = response.json()
        assert response_json['status'] == OrderStatus.APPROVED.value
        assert not response_json['estimated_arrival_time']

    @pytest.mark.django_db
    def test_update_order_status_to_approved_failed_when_order_has_hated_snacks(
        self, dummy_orders_set_1, dummy_snacks_set_1, dummy_snacks_reaction_set_1, member_user_1
    ):
        client = APIClient()
        client.force_authenticate(member_user_1)

        assert dummy_orders_set_1[0].status == OrderStatus.CREATED

        payload = {
            'status': OrderStatus.APPROVED.value,
        }
        response = client.patch(f'/orders/{dummy_orders_set_1[0].uid}/status/', data=payload, format='json')
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_update_order_status_to_approved_success_when_order_do_not_have_hated_snacks(
        self, dummy_orders_set_1, dummy_snacks_set_1, dummy_snacks_reaction_set_1, member_user_1
    ):
        client = APIClient()
        client.force_authenticate(member_user_1)

        assert dummy_orders_set_1[2].status == OrderStatus.CREATED

        payload = {
            'status': OrderStatus.APPROVED.value,
        }
        response = client.patch(f'/orders/{dummy_orders_set_1[2].uid}/status/', data=payload, format='json')
        assert response.status_code == 200


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


class TestSnackReactionViewSet:
    @pytest.mark.django_db
    def test_post_snack_reaction_viewset_create_reaction(self, dummy_snacks_set_1, member_user_1):
        """
        SnackReaction Model 을 deprecate 하면서 testcase 도 폐기
        """
        return
        client = APIClient()
        client.force_authenticate(member_user_1)
        payload = {'type': SnackReactionType.LIKE.value}
        response = client.post(f'/snacks/{dummy_snacks_set_1[0].uid}/reaction/', payload, format='json')
        assert response.status_code == 200

        snack_reaction = SnackReaction.objects.get(snack=dummy_snacks_set_1[0], user=member_user_1)
        assert snack_reaction.type == payload['type']

    @pytest.mark.django_db
    def test_post_snack_reaction_viewset_toggle_existing_reaction_to_opposite(
        self, dummy_snacks_set_1, dummy_snacks_reaction_set_1, member_user_1
    ):
        """
        SnackReaction Model 을 deprecate 하면서 testcase 도 폐기
        """
        return
        client = APIClient()
        client.force_authenticate(member_user_1)
        payload = {'type': SnackReactionType.LIKE.value}
        response = client.post(f'/snacks/{dummy_snacks_set_1[0].uid}/reaction/', payload, format='json')
        assert response.status_code == 200

        snack_reaction = SnackReaction.objects.get(snack=dummy_snacks_set_1[0], user=member_user_1)
        assert snack_reaction.type == payload['type']

    @pytest.mark.django_db
    def test_post_snack_reaction_viewset_toggle_update_count_fields(
        self, dummy_snacks_set_1, dummy_snacks_reaction_set_1, member_user_1
    ):
        return  # Because of add celery async logic

        client = APIClient()
        client.force_authenticate(member_user_1)
        payload = {'type': SnackReactionType.LIKE.value}
        response = client.post(f'/snacks/{dummy_snacks_set_1[0].uid}/reaction/', payload, format='json')
        assert response.status_code == 200

        updated_snack = Snack.objects.get(id=dummy_snacks_set_1[0].id)
        assert updated_snack.like_reaction_count == 4
        assert updated_snack.hate_reaction_count == 0

        payload = {'type': SnackReactionType.HATE.value}
        response = client.post(f'/snacks/{dummy_snacks_set_1[0].uid}/reaction/', payload, format='json')
        assert response.status_code == 200

        updated_snack = Snack.objects.get(id=dummy_snacks_set_1[0].id)
        assert updated_snack.like_reaction_count == 3
        assert updated_snack.hate_reaction_count == 1

    @pytest.mark.django_db
    def test_post_snack_reaction_viewset_response_400_if_same_type_reaction_exists(
        self, dummy_snacks_set_1, dummy_snacks_reaction_set_1, member_user_1
    ):
        """
        SnackReaction Model 을 deprecate 하면서 testcase 도 폐기
        """
        return
        client = APIClient()
        client.force_authenticate(member_user_1)
        payload = {'type': SnackReactionType.HATE.value}
        response = client.post(f'/snacks/{dummy_snacks_set_1[0].uid}/reaction/', payload, format='json')
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_post_snack_reaction_viewset_response_400_with_invalid_reaction_type(
        self, dummy_snacks_set_1, dummy_snacks_reaction_set_1, member_user_1
    ):
        client = APIClient()
        client.force_authenticate(member_user_1)
        payload = {'type': 'INVALIDTYPE'}
        response = client.post(f'/snacks/{dummy_snacks_set_1[0].uid}/reaction/', payload, format='json')
        assert response.status_code == 400


class TestGetTestOrderListView:
    @pytest.mark.django_db
    def test_get_test_order_list_response_status_200(
        self,
        member_user_1,
        test_order_item_1,
        test_order_item_2,
        test_order_item_3,
        test_order_item_4,
        test_order_item_5,
    ):
        client = APIClient()
        client.force_authenticate(member_user_1)

        response = client.get('/test-orders/')
        assert response.status_code == 200

        response_json = response.json()
        assert response_json
        assert len(response_json) == 5
        assert response_json[0]['uid'] == test_order_item_1.uid
        assert response_json[1]['uid'] == test_order_item_2.uid
        assert response_json[2]['uid'] == test_order_item_3.uid
        assert response_json[3]['uid'] == test_order_item_4.uid
        assert response_json[4]['uid'] == test_order_item_5.uid

    @pytest.mark.django_db
    def test_get_test_order_list_without_data_response_empty_list(
        self,
        member_user_1,
    ):
        client = APIClient()
        client.force_authenticate(member_user_1)

        response = client.get('/test-orders/')
        assert response.status_code == 200

        response_json = response.json()
        assert not response_json

    @pytest.mark.django_db
    def test_get_test_order_list_with_filter_response_filtered_data(
        self,
        member_user_1,
        test_order_item_1,
        test_order_item_2,
        test_order_item_3,
        test_order_item_4,
        test_order_item_5,
    ):
        client = APIClient()
        client.force_authenticate(member_user_1)

        response = client.get(f'/test-orders/?uid={test_order_item_4.uid}')
        assert response.status_code == 200

        response_json = response.json()
        assert response_json
        assert len(response_json) == 1
        assert response_json[0]['uid'] == test_order_item_4.uid
