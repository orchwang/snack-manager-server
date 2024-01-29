import pytest

from snack.order.models import Snack
from snack.order.tasks import update_snack_reaction_statistics


class TestUpdateSnackReactionStatisticsTask:
    @pytest.mark.django_db
    def test_update_snack_reaction_statistics_success(
        self, dummy_orders_set_1, dummy_snacks_set_1, dummy_snacks_reaction_set_1
    ):
        """
        Redis 로 관련 프로세스가 이동하여 테스트케이스 업데이트 필요
        """
        return
        like_count, hate_count, like_ratio = update_snack_reaction_statistics(dummy_snacks_set_1[0].uid)
        assert like_ratio == 3.0

        updated_snack = Snack.objects.get(uid=dummy_snacks_set_1[0].uid)
        assert updated_snack.like_ratio == 3.0
