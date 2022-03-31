from http import HTTPStatus
from typing import Tuple

from flask_restx import Resource as RestxResource
from conf import settings
from . import api


@api.route("")
class UserList(RestxResource):
    def get(self) -> Tuple[dict, int]:
        return {"request": "ok", "secret_code": settings.SECRET_CODE}, HTTPStatus.BAD_REQUEST
