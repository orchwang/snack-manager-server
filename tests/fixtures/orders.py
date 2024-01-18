import json

import pytest
from django.conf import settings
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

from snack.order.constants import Currency, SnackReactionType
from snack.order.models import Snack, Order, Purchase, SnackReaction


@pytest.fixture
def dummy_snacks_set_1():
    snacks_json_path = f'{settings.TEST_DIR}/fixtures/snacks_raw_data/snacks.json'
    with open(snacks_json_path, 'r') as json_file:
        snacks_data = json.load(json_file)
    snack_list = []
    for snack_data in snacks_data:
        image = File(
            open(
                f"{settings.TEST_DIR}/fixtures/snacks_raw_data/{snack_data.get('image')}",
                'rb',
            )
        )
        upload_image = SimpleUploadedFile(snack_data.get('image'), image.read(), content_type='multipart/form-data')
        snack_list.append(
            Snack(
                name=snack_data.get('name'),
                url=snack_data.get('url'),
                image=upload_image,
                desc=snack_data.get('desc'),
                price=snack_data.get('price'),
                currency=Currency(snack_data.get('currency')),
            )
        )
    return Snack.objects.bulk_create(snack_list)


@pytest.fixture
def dummy_orders_set_1(dummy_snacks_set_1, member_user_1, member_user_2, member_user_3, member_user_4):
    order_list = []

    order_list.append(Order(user=member_user_1))
    order_list.append(Order(user=member_user_1))
    order_list.append(Order(user=member_user_2))
    order_list.append(Order(user=member_user_3))
    order_list.append(Order(user=member_user_4))

    orders = Order.objects.bulk_create(order_list)

    purchase_list = []

    purchase_list.append(Purchase(order=orders[0], snack=dummy_snacks_set_1[0], quantity=1))
    purchase_list.append(Purchase(order=orders[0], snack=dummy_snacks_set_1[2], quantity=1))
    purchase_list.append(Purchase(order=orders[0], snack=dummy_snacks_set_1[3], quantity=1))

    purchase_list.append(Purchase(order=orders[1], snack=dummy_snacks_set_1[2], quantity=4))
    purchase_list.append(Purchase(order=orders[1], snack=dummy_snacks_set_1[4], quantity=4))

    purchase_list.append(Purchase(order=orders[2], snack=dummy_snacks_set_1[0], quantity=20))
    purchase_list.append(Purchase(order=orders[2], snack=dummy_snacks_set_1[1], quantity=20))
    purchase_list.append(Purchase(order=orders[2], snack=dummy_snacks_set_1[3], quantity=20))
    purchase_list.append(Purchase(order=orders[2], snack=dummy_snacks_set_1[4], quantity=20))

    purchase_list.append(Purchase(order=orders[3], snack=dummy_snacks_set_1[0], quantity=50))
    purchase_list.append(Purchase(order=orders[3], snack=dummy_snacks_set_1[1], quantity=50))
    purchase_list.append(Purchase(order=orders[3], snack=dummy_snacks_set_1[2], quantity=50))
    purchase_list.append(Purchase(order=orders[3], snack=dummy_snacks_set_1[3], quantity=50))
    purchase_list.append(Purchase(order=orders[3], snack=dummy_snacks_set_1[4], quantity=50))

    purchase_list.append(Purchase(order=orders[4], snack=dummy_snacks_set_1[0], quantity=15))
    purchase_list.append(Purchase(order=orders[4], snack=dummy_snacks_set_1[2], quantity=15))
    purchase_list.append(Purchase(order=orders[4], snack=dummy_snacks_set_1[3], quantity=15))
    purchase_list.append(Purchase(order=orders[4], snack=dummy_snacks_set_1[4], quantity=15))

    Purchase.objects.bulk_create(purchase_list)

    return orders


@pytest.fixture
def dummy_snacks_reaction_set_1(dummy_snacks_set_1, member_user_1, member_user_2, member_user_3, member_user_4):
    reactions_list = []

    reactions_list.append(SnackReaction(snack=dummy_snacks_set_1[0], user=member_user_1, type=SnackReactionType.HATE))
    reactions_list.append(SnackReaction(snack=dummy_snacks_set_1[0], user=member_user_2, type=SnackReactionType.LIKE))
    reactions_list.append(SnackReaction(snack=dummy_snacks_set_1[0], user=member_user_3, type=SnackReactionType.LIKE))
    reactions_list.append(SnackReaction(snack=dummy_snacks_set_1[0], user=member_user_4, type=SnackReactionType.LIKE))

    reactions_list.append(SnackReaction(snack=dummy_snacks_set_1[1], user=member_user_1, type=SnackReactionType.LIKE))
    reactions_list.append(SnackReaction(snack=dummy_snacks_set_1[1], user=member_user_2, type=SnackReactionType.HATE))
    reactions_list.append(SnackReaction(snack=dummy_snacks_set_1[1], user=member_user_3, type=SnackReactionType.HATE))
    reactions_list.append(SnackReaction(snack=dummy_snacks_set_1[1], user=member_user_4, type=SnackReactionType.LIKE))

    reactions_list.append(SnackReaction(snack=dummy_snacks_set_1[2], user=member_user_1, type=SnackReactionType.LIKE))
    reactions_list.append(SnackReaction(snack=dummy_snacks_set_1[2], user=member_user_2, type=SnackReactionType.HATE))
    reactions_list.append(SnackReaction(snack=dummy_snacks_set_1[2], user=member_user_3, type=SnackReactionType.HATE))
    reactions_list.append(SnackReaction(snack=dummy_snacks_set_1[2], user=member_user_4, type=SnackReactionType.HATE))

    reactions_list.append(SnackReaction(snack=dummy_snacks_set_1[3], user=member_user_1, type=SnackReactionType.LIKE))
    reactions_list.append(SnackReaction(snack=dummy_snacks_set_1[3], user=member_user_3, type=SnackReactionType.HATE))
    reactions_list.append(SnackReaction(snack=dummy_snacks_set_1[3], user=member_user_4, type=SnackReactionType.LIKE))

    reactions_list.append(SnackReaction(snack=dummy_snacks_set_1[4], user=member_user_1, type=SnackReactionType.LIKE))
    reactions_list.append(SnackReaction(snack=dummy_snacks_set_1[4], user=member_user_4, type=SnackReactionType.LIKE))

    snack_reactions = SnackReaction.objects.bulk_create(reactions_list)
    return snack_reactions
