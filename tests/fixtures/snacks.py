import json

import pytest
from django.conf import settings
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.backends.sqlite3.base import *

from snack.order.constants import Currency
from snack.order.models import Snack


@pytest.fixture
def dummy_snacks_set_1():
    snacks_json_path = f"{settings.TEST_DIR}/fixtures/snacks_raw_data/snacks.json"
    with open(snacks_json_path, "r") as json_file:
        snacks_data = json.load(json_file)
    snack_list = []
    for snack_data in snacks_data:
        image = File(
            open(
                f"{settings.TEST_DIR}/fixtures/snacks_raw_data/{snack_data.get('image')}",
                "rb",
            )
        )
        upload_image = SimpleUploadedFile(
            snack_data.get("image"), image.read(), content_type="multipart/form-data"
        )
        snack_list.append(
            Snack(
                name=snack_data.get("name"),
                url=snack_data.get("url"),
                image=upload_image,
                price=snack_data.get("price"),
                currency=Currency(snack_data.get("currency")),
            )
        )
    return Snack.objects.bulk_create(snack_list)
