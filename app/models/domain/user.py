from dataclasses import dataclass
import uuid

@dataclass
class User:
    id: uuid.UUID
    email: str
    is_superuser: bool
    full_name: str | None
