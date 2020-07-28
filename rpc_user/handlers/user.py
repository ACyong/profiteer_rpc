# -*- coding:utf-8 -*-
from rpc_user.models.user import User


class UserHandler(object):
    @classmethod
    def create_user(cls, user):
        payload = {k: v for k, v in user.__dict__.items() if v is not None}
        if not payload:
            return
        user_id = payload.pop("user_id", None)
        if not user_id:
            return
        User.create(user_id, payload)
