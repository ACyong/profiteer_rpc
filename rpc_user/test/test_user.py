# -*- coding: utf-8 -*-
from rpc_user.models.user import User


class TestUser(object):
    def test_create(self):
        user_id = 1701
        payload = dict()
        User.create(user_id, payload)
        result = User.get(user_id)
        assert result
