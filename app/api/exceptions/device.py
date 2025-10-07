from fastapi import HTTPException, status


class ErrDeviceTypeExists(HTTPException):
    def __init__(self, name: str | None = None) -> None:
        if name:
            detail = f"Device type with name '{name}' already exists"
        else:
            detail = "Device type with this name already exists"

        super().__init__(status.HTTP_400_BAD_REQUEST, detail)


class ErrNotDeviceOwner(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the owner of this device",
        )


class ErrDeviceNotFound(HTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, "Device not found")
