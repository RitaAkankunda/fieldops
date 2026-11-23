import pytest
from django.contrib.auth import get_user_model


def test_user_has_technician_role_by_default():
    User = get_user_model()

    user = User(username="grace")

    assert user.role == "TECHNICIAN"


def test_user_can_have_admin_role():
    User = get_user_model()

    user = User(username="sarah", role="ADMIN")

    assert user.role == "ADMIN"


def test_admin_role_does_not_grant_superuser_privileges():
    User = get_user_model()

    user = User(username="sarah", role="ADMIN")

    assert user.is_superuser is False
    assert user.is_staff is False


@pytest.mark.django_db
def test_user_can_be_saved_and_retrieved():
    # Arrange
    User = get_user_model()

    # Act
    user = User.objects.create_user(
        username="grace",
        password="TestPassword123!"
    )

    retrieved_user = User.objects.get(pk=user.pk)

    # Assert
    assert retrieved_user.username == "grace"
    assert retrieved_user.role == "TECHNICIAN"
    assert retrieved_user.check_password("TestPassword123!")