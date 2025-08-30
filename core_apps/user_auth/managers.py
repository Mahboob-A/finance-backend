import random
import string
from os import getenv
from typing import Any, Optional

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


def generate_username() -> str:
    """Generate a random username with the bank name as prefix."""

    # Bank Of Finance
    bank_name = getenv("BANK_NAME", "Bank of Finance")

    # ["Bank", "Of", "Finance"]
    words = bank_name.split()

    # BOF
    prefix = "".join(word[0].upper() for word in words).upper()

    # the username should be 16 characters long. 1 is reserved for the dash "-"
    remaining_length = 16 - len(prefix) - 1

    # X7O6QFT8F55R
    random_string = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=remaining_length)
    )

    # BOF-X7O6QFT8F55R
    username = f"{prefix}-{random_string}"

    return username



def validate_email_address(email: str) -> None:
    """Validate the email address format."""
    try:
        validate_email(email)
    except ValidationError:
        raise ValidationError(_("Enter a valid email address."))



class UserManager(DjangoUserManager):
    """Custom user manager for the User model."""

    def _create_user(
        self,
        email: str,
        password: Optional[str] = None,
        **extra_fields: Any,
    ) -> Any:
        """Create and return a user with an email and password."""
        if not email:
            raise ValueError(_("The Email field must be provided."))
        
        if not password:
            raise ValueError(_("The Password field must be provided."))

        username = generate_username()

        email = self.normalize_email(email)

        validate_email_address(email)

        user = self.model(email=email, username=username, **extra_fields)

        user.password = make_password(password)

        user.save(using=self._db)

        return user

    def create(self, email: str, password: Optional[str] = None, **extra_fields: Any) -> Any:
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email=email, password=password, **extra_fields)

    def create_superuser(
        self, email: str, password: Optional[str] = None, **extra_fields: Any
    ) -> Any:
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(email=email, password=password, **extra_fields)