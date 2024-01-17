from rest_framework.exceptions import APIException


class InvalidEmail(APIException):
    status_code = 400
    default_detail = 'Invalid email.'


class InvalidRequest(APIException):
    status_code = 400
    default_detail = 'Invalid Request.'
