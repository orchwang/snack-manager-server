import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def member_user_1():
    user = User.objects.create_user('test_member_user_1', 'test_member_user_1@test.com', 'password')
    user.first_name = 'testmember1'
    user.last_name = 'hwang'
    user.save()
    return user
