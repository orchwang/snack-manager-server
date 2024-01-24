# Generated by Django 4.2.9 on 2024-01-24 06:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('order', '0018_alter_snack_hate_reaction_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='day',
            field=models.IntegerField(help_text='통계 처리를 위한 생성일시 기준 일 값', null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='month',
            field=models.IntegerField(help_text='통계 처리를 위한 생성일시 기준 월 값', null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='year',
            field=models.IntegerField(help_text='통계 처리를 위한 생성일시 기준 연도 값', null=True),
        ),
    ]
