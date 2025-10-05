from fastapi import HTTPException, status


class ErrUserExists(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            "The user with this email already exists in the system",
        )


class ErrUnauthorized(HTTPException):
    def __init__(self, detail: str = "Unauthorized") -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail)


class ErrNotEnoughPrivileges(HTTPException):
    def __init__(self, detail: str = "You don't have enough privileges") -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, detail)


class ErrUserNotFound(HTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, "User not found")
