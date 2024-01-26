from django.apps import apps
from django.core.cache import cache

from snack.celery import app
from snack.order.constants import SnackReactionType


@app.task
def update_snack_reaction_statistics(snack_uid: str):
    Snack = apps.get_model('order', 'Snack')
    snack = Snack.objects.get(uid=snack_uid)

    like_count = cache.get(f'{snack.uid}-{SnackReactionType.LIKE.value}')
    hate_count = cache.get(f'{snack.uid}-{SnackReactionType.HATE.value}')

    snack.like_reaction_count = like_count
    snack.hate_reaction_count = hate_count
    if not hate_count:
        like_ratio = like_count
    else:
        like_ratio = like_count / hate_count

    snack.like_reaction_count = like_count
    snack.hate_reaction_count = hate_count
    snack.like_ratio = like_ratio
    snack.save()

    return like_count, hate_count, like_ratio
