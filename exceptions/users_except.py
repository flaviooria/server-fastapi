from typing import List

__all__ = (
    "MSG_ERROR_USER_NOT_FOUND",
    "MSG_ERROR_USER_NOT_CREATED",
    "MSG_ERROR_USER_NOT_UPDATED",
    "MSG_ERROR_USER_NOT_DELETED",
)


MSG_ERROR_USER_NOT_FOUND = 'User not found'
MSG_ERROR_USER_NOT_CREATED = 'User not created'
MSG_ERROR_USER_NOT_UPDATED = 'User not updated'
MSG_ERROR_USER_NOT_DELETED = 'User not deleted'


def __dir__() -> List[str]:
    return sorted(list(__all__))