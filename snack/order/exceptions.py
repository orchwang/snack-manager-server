from rest_framework.exceptions import APIException


class InvalidSnack(APIException):
    status_code = 400
    default_detail = 'Invalid snack.'


class InvalidSnackReaction(APIException):
    status_code = 400
    default_detail = 'Invalid snack reaction.'
