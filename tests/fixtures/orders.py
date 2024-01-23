import json
from typing import Optional

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

from snack.order.constants import Currency, SnackReactionType
from snack.order.models import Snack, Order, Purchase, SnackReaction

User = get_user_model()


@pytest.fixture
def dummy_snacks_set_1():
    """
    TODO: 단일 메소드에 복수의 fixture 를 생성할 경우 Testcase 마다
          생성하는 데이터가 불필요하게 많아져 비효율을 발생시킨다.
          메소드가 많아지더라도 별도 생성하여 관리하는 것이 좋겠다.
          메소드가 많아지면 fixture 를 구조화 하여 잘 나누면 된다.
    """
    snacks_json_path = f'{settings.TEST_DIR}/fixtures/snacks_raw_data/snacks.json'
    with open(snacks_json_path, 'r') as json_file:
        snacks_data = json.load(json_file)

    created_snacks_ids = []
    for snack_data in snacks_data:
        image = File(
            open(
                f"{settings.TEST_DIR}/fixtures/snacks_raw_data/{snack_data.get('image')}",
                'rb',
            )
        )
        upload_image = SimpleUploadedFile(snack_data.get('image'), image.read(), content_type='multipart/form-data')
        obj = Snack(
            name=snack_data.get('name'),
            url=snack_data.get('url'),
            image=upload_image,
            desc=snack_data.get('desc'),
            price=snack_data.get('price'),
            currency=Currency(snack_data.get('currency')),
        )
        obj.save()
        created_snacks_ids.append(obj.id)

    return Snack.objects.filter(id__in=created_snacks_ids)


@pytest.fixture
def dummy_orders_set_1(dummy_snacks_set_1, member_user_1, member_user_2, member_user_3, member_user_4):
    members_list = [member_user_1, member_user_1, member_user_2, member_user_3, member_user_4]
    order_ids_list = []
    for member in members_list:
        obj = Order(user=member)
        obj.save()
        order_ids_list.append(obj.id)

    orders = Order.objects.filter(id__in=order_ids_list).all()

    purchase_ids_list = []

    def create_purchase_row(order: Optional[Order], snack: Optional[Snack], quantity: int):
        created_purchase = Purchase(order=order, snack=snack, quantity=quantity)
        created_purchase.save()
        purchase_ids_list.append(obj.id)

    create_purchase_row(orders[0], dummy_snacks_set_1[2], 1)
    create_purchase_row(orders[0], dummy_snacks_set_1[3], 1)

    create_purchase_row(orders[1], dummy_snacks_set_1[2], 4)
    create_purchase_row(orders[1], dummy_snacks_set_1[4], 4)

    create_purchase_row(orders[2], dummy_snacks_set_1[0], 20)
    create_purchase_row(orders[2], dummy_snacks_set_1[1], 20)
    create_purchase_row(orders[2], dummy_snacks_set_1[3], 20)
    create_purchase_row(orders[2], dummy_snacks_set_1[4], 20)

    create_purchase_row(orders[3], dummy_snacks_set_1[0], 50)
    create_purchase_row(orders[3], dummy_snacks_set_1[1], 50)
    create_purchase_row(orders[3], dummy_snacks_set_1[2], 50)
    create_purchase_row(orders[3], dummy_snacks_set_1[3], 50)
    create_purchase_row(orders[3], dummy_snacks_set_1[4], 50)

    create_purchase_row(orders[4], dummy_snacks_set_1[0], 15)
    create_purchase_row(orders[4], dummy_snacks_set_1[2], 15)
    create_purchase_row(orders[4], dummy_snacks_set_1[3], 15)
    create_purchase_row(orders[4], dummy_snacks_set_1[4], 15)

    return orders


@pytest.fixture
def dummy_snacks_reaction_set_1(dummy_snacks_set_1, member_user_1, member_user_2, member_user_3, member_user_4):
    reactions_list = []

    def create_snack_reaction_row(snack: Optional[Snack], user: Optional[User], type: Optional[SnackReactionType]):
        created_obj = SnackReaction(snack=snack, user=user, type=type)
        created_obj.save()
        reactions_list.append(created_obj.id)

    create_snack_reaction_row(dummy_snacks_set_1[0], member_user_1, SnackReactionType.HATE)
    create_snack_reaction_row(dummy_snacks_set_1[0], member_user_2, SnackReactionType.LIKE)
    create_snack_reaction_row(dummy_snacks_set_1[0], member_user_3, SnackReactionType.LIKE)
    create_snack_reaction_row(dummy_snacks_set_1[0], member_user_4, SnackReactionType.LIKE)

    create_snack_reaction_row(dummy_snacks_set_1[1], member_user_1, SnackReactionType.LIKE)
    create_snack_reaction_row(dummy_snacks_set_1[1], member_user_2, SnackReactionType.HATE)
    create_snack_reaction_row(dummy_snacks_set_1[1], member_user_3, SnackReactionType.HATE)
    create_snack_reaction_row(dummy_snacks_set_1[1], member_user_4, SnackReactionType.LIKE)

    create_snack_reaction_row(dummy_snacks_set_1[2], member_user_1, SnackReactionType.LIKE)
    create_snack_reaction_row(dummy_snacks_set_1[2], member_user_2, SnackReactionType.HATE)
    create_snack_reaction_row(dummy_snacks_set_1[2], member_user_3, SnackReactionType.HATE)
    create_snack_reaction_row(dummy_snacks_set_1[2], member_user_4, SnackReactionType.HATE)

    create_snack_reaction_row(dummy_snacks_set_1[3], member_user_1, SnackReactionType.LIKE)
    create_snack_reaction_row(dummy_snacks_set_1[3], member_user_3, SnackReactionType.HATE)
    create_snack_reaction_row(dummy_snacks_set_1[3], member_user_4, SnackReactionType.LIKE)

    create_snack_reaction_row(dummy_snacks_set_1[4], member_user_1, SnackReactionType.LIKE)
    create_snack_reaction_row(dummy_snacks_set_1[4], member_user_4, SnackReactionType.LIKE)

    snack_reactions = SnackReaction.objects.filter(id__in=reactions_list).all()

    # Update Order count fields
    for snack in dummy_snacks_set_1:
        like_count = snack.get_like_reaction_count()
        hate_count = snack.get_hate_reaction_count()
        if hate_count:
            like_ratio = like_count / hate_count
        else:
            like_ratio = like_count
        snack.like_reaction_count = like_count
        snack.hate_reaction_count = hate_count
        snack.like_ratio = like_ratio
        snack.save()

    return snack_reactions
