from typing import List

__all__ = (
    "MSG_ERROR_USER_NOT_FOUND",
    "MSG_ERROR_USER_NOT_CREATED",
    "MSG_ERROR_USER_NOT_UPDATED",
    "MSG_ERROR_USER_NOT_DELETED",
    "MSG_ERROR_USER_NOT_CORRECT",
    "MSG_ERROR_USER_NOT_AUTHORIZED",
    "MSG_ERROR_USER_PASSWORD_INCORRECT",
    "MSG_ERROR_USER_INACTIVE"
)


MSG_ERROR_USER_NOT_FOUND = 'User not found'
MSG_ERROR_USER_NOT_CREATED = 'User not created'
MSG_ERROR_USER_NOT_UPDATED = 'User not updated'
MSG_ERROR_USER_NOT_DELETED = 'User not deleted'
MSG_ERROR_USER_NOT_CORRECT = 'User is not correct'
MSG_ERROR_USER_NOT_AUTHORIZED = 'User\'s credentials not authorized'
MSG_ERROR_USER_PASSWORD_INCORRECT = 'User\'s password incorrect'
MSG_ERROR_USER_INACTIVE = 'User inactive'


def __dir__() -> List[str]:
    return sorted(list(__all__))