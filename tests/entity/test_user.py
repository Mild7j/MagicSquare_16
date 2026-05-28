"""Tests for the User entity."""

import pytest

from src.entity.user import User


def test_create_returns_valid_user() -> None:
    # Arrange
    user_id = 1
    name = "Alice"
    email = "alice@example.com"

    # Act
    user = User.create(user_id=user_id, name=name, email=email)

    # Assert
    assert user.user_id == 1
    assert user.name == "Alice"
    assert user.email == "alice@example.com"


def test_create_raises_when_user_id_is_not_positive() -> None:
    # Arrange
    user_id = 0

    # Act / Assert
    with pytest.raises(ValueError, match="user_id must be greater than zero."):
        User.create(user_id=user_id, name="Alice", email="alice@example.com")


def test_create_raises_when_name_is_blank() -> None:
    # Arrange
    name = "   "

    # Act / Assert
    with pytest.raises(ValueError, match="name must not be blank."):
        User.create(user_id=1, name=name, email="alice@example.com")


def test_create_raises_when_email_is_invalid() -> None:
    # Arrange
    email = "invalid-email"

    # Act / Assert
    with pytest.raises(ValueError, match="email must be a valid email format."):
        User.create(user_id=1, name="Alice", email=email)


def test_rename_returns_new_user_with_updated_name() -> None:
    # Arrange
    original = User.create(user_id=1, name="Alice", email="alice@example.com")
    new_name = "Bob"

    # Act
    renamed = original.rename(new_name)

    # Assert
    assert renamed.name == "Bob"
    assert renamed.email == "alice@example.com"
    assert renamed.user_id == 1
    assert renamed is not original


def test_change_email_returns_new_user_with_updated_email() -> None:
    # Arrange
    original = User.create(user_id=1, name="Alice", email="alice@example.com")
    new_email = "bob@example.com"

    # Act
    updated = original.change_email(new_email)

    # Assert
    assert updated.email == "bob@example.com"
    assert updated.name == "Alice"
    assert updated.user_id == 1
    assert updated is not original


def test_to_dict_returns_expected_mapping() -> None:
    # Arrange
    user = User.create(user_id=7, name="Carol", email="carol@example.com")

    # Act
    user_dict = user.to_dict()

    # Assert
    assert user_dict == {
        "user_id": 7,
        "name": "Carol",
        "email": "carol@example.com",
    }
