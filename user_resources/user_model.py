from dataclasses import dataclass, field
from typing import Optional


@dataclass
class User:
    username: str
    password: str
    token: Optional[str] = field(default=None)
    name: str = field(default=None)
    surname: str = field(default=None)
    date_of_birth: str = field(default=None)
    registered: bool = field(default=False)
    iban: str = field(default=None)
    id: int = field(default=None)

    def save_to_file(self):
        return {"username": self.username,
                "password": self.password,
                "name": self.name,
                "surname": self.surname,
                "date_of_birth": self.date_of_birth,
                "iban": self.iban,
                "id": self.id}
