"""User entity for the MagicSquare domain."""

from __future__ import annotations

from dataclasses import dataclass
from re import Pattern, compile

EMAIL_PATTERN: Pattern[str] = compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MAX_NAME_LENGTH = 50


@dataclass(frozen=True, slots=True)
class User:
    """Represents a validated user in the domain layer.

    Attributes:
        user_id: Positive unique identifier for a user.
        name: Display name of the user.
        email: Email address of the user.
    """

    user_id: int
    name: str
    email: str

    def __post_init__(self) -> None:
        """Validate domain invariants immediately after initialization."""
        self._validate_user_id(self.user_id)
        self._validate_name(self.name)
        self._validate_email(self.email)

    @classmethod
    def create(cls, user_id: int, name: str, email: str) -> "User":
        """Create a new validated user entity.

        Args:
            user_id: Positive unique identifier for a user.
            name: Display name of the user.
            email: Email address of the user.

        Returns:
            User: A validated user instance.
        """
        return cls(user_id=user_id, name=name, email=email)

    def rename(self, new_name: str) -> "User":
        """Return a new user with an updated name.

        Args:
            new_name: New display name.

        Returns:
            User: A new user instance with updated name.
        """
        self._validate_name(new_name)
        return User(user_id=self.user_id, name=new_name, email=self.email)

    def change_email(self, new_email: str) -> "User":
        """Return a new user with an updated email.

        Args:
            new_email: New email address.

        Returns:
            User: A new user instance with updated email.
        """
        self._validate_email(new_email)
        return User(user_id=self.user_id, name=self.name, email=new_email)

    def to_dict(self) -> dict[str, int | str]:
        """Convert this user entity to a plain dictionary.

        Returns:
            dict[str, int | str]: Dictionary representation of user fields.
        """
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
        }

    @staticmethod
    def _validate_user_id(user_id: int) -> None:
        if user_id <= 0:
            raise ValueError("user_id must be greater than zero.")

    @staticmethod
    def _validate_name(name: str) -> None:
        normalized_name = name.strip()
        if not normalized_name:
            raise ValueError("name must not be blank.")
        if len(normalized_name) > MAX_NAME_LENGTH:
            raise ValueError(f"name must be at most {MAX_NAME_LENGTH} characters.")

    @staticmethod
    def _validate_email(email: str) -> None:
        normalized_email = email.strip()
        if not normalized_email:
            raise ValueError("email must not be blank.")
        if EMAIL_PATTERN.fullmatch(normalized_email) is None:
            raise ValueError("email must be a valid email format.")
