import re
from datetime import datetime

import pytest
from pydantic import ValidationError

from app.domain.entities.user import User
from app.domain.exceptions import InvalidPhoneNumberException


def test_user_create():
    user = User(
        name='name',
        surname='surname',
        username='username',
        phone_number='+375444276532',
        email='qwertyusdfg@gmail.com',
        role_id=2,
        group_id=1,
        image_path='',
        is_blocked=False,
        active=True,
        id=1,
        created_at=datetime.now(),
        modified_at=datetime.now(),
    )
    assert user
    assert user.name == "name"
    assert user.surname == "surname"
    assert user.username == 'username'
    assert user.phone_number == "+375444276532"
    assert user.email == "qwertyusdfg@gmail.com"
    assert user.role_id == 2
    assert user.group_id == 1
    assert user.image_path == ''
    assert user.is_blocked is False
    assert user.active is True
    assert user.id == 1


def test_user_create_throws_invalid_email_exception():
    with pytest.raises(ValidationError) as exc:
        user = User(
            name='name',
            surname='surname',
            username='username',
            phone_number='+375444276532',
            email='qwertyusdfg@',
            role_id=2,
            group_id=1,
            image_path='',
            is_blocked=False,
            active=True,
            id=1,
            created_at=datetime.now(),
            modified_at=datetime.now(),
        )
    assert exc.value.errors()[0]["loc"][0] == "email"
    assert exc.value.errors()[0][
               "msg"] == "value is not a valid email address: There must be something after the @-sign."


def test_customer_create_throws_invalid_phone_exception():
    with pytest.raises(InvalidPhoneNumberException) as exc:
        user = User(
            name='name',
            surname='surname',
            username='username',
            phone_number='5663434525234363',
            email='qwertyusdfg@gmail.com',
            role_id=2,
            group_id=1,
            image_path='',
            is_blocked=False,
            active=True,
            id=1,
            created_at=datetime.now(),
            modified_at=datetime.now(),
        )
    assert isinstance(exc.value, InvalidPhoneNumberException)

