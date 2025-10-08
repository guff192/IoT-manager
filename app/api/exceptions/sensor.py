from fastapi import HTTPException, status


class ErrSensorTypeExists(HTTPException):
    def __init__(self, name: str | None = None) -> None:
        if name:
            detail = f"Sensor type with name '{name}' already exists"
        else:
            detail = "Sensor type with this name already exists"

        super().__init__(status.HTTP_400_BAD_REQUEST, detail)


class ErrNotSensorOwner(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the owner of this sensor",
        )


class ErrSensorNotFound(HTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, "Sensor not found")
