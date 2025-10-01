from fastapi import HTTPException, status


class ErrServiceUnavailable(HTTPException):
    def __init__(self, detail="Service Unavailable"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail,
        )
