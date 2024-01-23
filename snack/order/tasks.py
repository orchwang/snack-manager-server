from snack.order.models import Snack

from snack.celery import app


@app.task
def update_snack_reaction_statistics(snack_uid):
    snack = Snack.objects.get(uid=snack_uid)
    like_count = snack.get_like_reaction_count()
    hate_count = snack.get_hate_reaction_count()
    # snack.like_reaction_count = like_count
    # snack.hate_reaction_count = hate_count
    if not hate_count:
        like_ratio = like_count
    else:
        like_ratio = like_count / hate_count
    snack.like_ratio = like_ratio
    snack.save()

    return like_count, hate_count, like_ratio
