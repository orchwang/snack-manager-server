import pytest

from snack.order.models import Snack
from snack.order.tasks import update_snack_reaction_statistics


class TestUpdateSnackReactionStatisticsTask:
    @pytest.mark.django_db
    def test_update_snack_reaction_statistics_success(
        self, dummy_orders_set_1, dummy_snacks_set_1, dummy_snacks_reaction_set_1
    ):
        like_count, hate_count, like_ratio = update_snack_reaction_statistics(dummy_snacks_set_1[0].uid)
        assert like_count == 3
        assert hate_count == 1
        assert like_ratio == 3.0

        updated_snack = Snack.objects.get(uid=dummy_snacks_set_1[0].uid)
        assert updated_snack.like_reaction_count == 3
        assert updated_snack.hate_reaction_count == 1
        assert updated_snack.like_ratio == 3.0
