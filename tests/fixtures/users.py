import pytest
from django.contrib.auth import get_user_model

from snack import MemberType

User = get_user_model()


@pytest.fixture
def member_user_1():
    user = User.objects.create_user('test_member_user_1', 'test_member_user_1@test.com', 'password')
    user.first_name = 'testmember1'
    user.last_name = 'hwang'
    user.member_type = MemberType.ADMIN
    user.save()
    return user


@pytest.fixture
def member_user_2():
    user = User.objects.create_user('test_member_user_2', 'test_member_user_2@test.com', 'password')
    user.first_name = 'testmember2'
    user.last_name = 'park'
    user.member_type = MemberType.MEMBER
    user.save()
    return user


@pytest.fixture
def member_user_3():
    user = User.objects.create_user('test_member_user_3', 'test_member_user_3@test.com', 'password')
    user.first_name = 'testmember3'
    user.last_name = 'kim'
    user.member_type = MemberType.MEMBER
    user.save()
    return user


@pytest.fixture
def member_user_4():
    user = User.objects.create_user('test_member_user_4', 'test_member_user_4@test.com', 'password')
    user.first_name = 'testmember4'
    user.last_name = 'lee'
    user.member_type = MemberType.MEMBER
    user.save()
    return user
