import json

import pytest
from django.conf import settings


class TestDummyView:
    @pytest.mark.django_db
    def test_dummy_snacks_fixtures_created_properly(self, dummy_snacks_set_1):
        snacks_json_path = f"{settings.TEST_DIR}/fixtures/snacks_raw_data/snacks.json"

        with open(snacks_json_path, "r") as json_file:
            snacks_data = json.load(json_file)

        i = 0
        for data in snacks_data:
            assert data["name"] == dummy_snacks_set_1[i].name
            i += 1
