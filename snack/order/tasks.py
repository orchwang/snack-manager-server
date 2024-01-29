from django.apps import apps

from django_redis import get_redis_connection

from snack.celery import app


@app.task
def update_snack_reaction_statistics(snack_uid: str):
    Snack = apps.get_model('order', 'Snack')
    snack = Snack.objects.get(uid=snack_uid)

    redis_con = get_redis_connection('default')

    like_key = f'snack:like:{snack.id}'
    hate_key = f'snack:hate:{snack.id}'

    like_count = redis_con.scard(like_key)
    hate_count = redis_con.scard(hate_key)

    if not hate_count:
        like_ratio = like_count
    else:
        like_ratio = like_count / hate_count

    snack.like_reaction_count = like_count
    snack.hate_reaction_count = hate_count
    snack.like_ratio = like_ratio
    snack.save()

    return like_count, hate_count, like_ratio
