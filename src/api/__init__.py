import logging
from http import HTTPStatus

from flask import Blueprint
from flask_restx import Api
from werkzeug.exceptions import BadRequest, Forbidden, NotFound, Unauthorized

from .user.endpoints import api as user_api

blueprint = Blueprint("api", __name__)

authorizations = {
    "Authorization": {
        "description": "Inputs: Basic user=\\<email\\> or Bearer \\<jwtToken\\>",
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
    }
}

api = Api(
    blueprint,
    title="Proizer API",
    version="1.0",
    description="Proizer APIs",
    authorizations=authorizations,
    security="Authorization",
)
api.add_namespace(user_api)


@api.errorhandler(BadRequest)
def handle_bad_request_error(exception_cause):
    """
    Catch bad request error exception globally and respond with 400.

    :param exception_cause:
    :return objects, response Code:
    """
    if hasattr(exception_cause, "data") and "errors" in exception_cause.data.keys():
        all_errors = exception_cause.data["errors"]
        errors = []
        for each in all_errors.keys():
            if each and "." in each and len(each.split(".")) >= 3:
                errors.append(f"{each.split('.')[2]} : {all_errors[each]}")
            elif each:
                errors.append(f"{each} : {all_errors[each]}")
            else:
                errors.append("extra field not allowed")

        exception_cause.data.update(failure(errors))
        return exception_cause.data, HTTPStatus.BAD_REQUEST
    else:
        return exception_cause.description, HTTPStatus.BAD_REQUEST


@api.errorhandler(NotFound)
def handle_not_found_error(exception_cause):
    """
    Catch not found error exception globally and respond with 404.
    :param exception_cause:
    :return objects, response Code:
    """
    logging.exception(exception_cause)
    return exception_cause.description, HTTPStatus.NOT_FOUND


@api.errorhandler(Unauthorized)
def handle_unauthorized_error(exception_cause):
    """
    Catch unauthorized globally and respond with 401.
    :param exception_cause:
    :return objects , response Code:
    """
    logging.exception(exception_cause)
    return exception_cause.description, HTTPStatus.UNAUTHORIZED


@api.errorhandler(Forbidden)
def handle_forbidden_error(exception_cause):
    """
    Catch forbidden globally and respond with 403.
    :param exception_cause:
    :return objects , response Code:
    """
    logging.exception(exception_cause)
    return exception_cause.description, HTTPStatus.FORBIDDEN
