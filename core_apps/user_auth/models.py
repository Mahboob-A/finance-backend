import uuid 

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from user_auth.emails import send_account_locked_email
from user_auth.managers import UserManager



# Create your models here.
class User(AbstractUser):
    class SecurityQuestions(models.TextChoices):
        MAIDEN_NAME = (
            "maiden_name", 
            _("What is your mother's maiden name?")
        )
        FAVORITE_COLOR = (
            "favorite_color", 
            _("What is your favorite color?")
        )
        BIRTH_CITY = (
            "birth_city", 
            _("What is your birth city?")
        )
        CHILDHOOD_FRIEND = (
            "childhood_friend", 
            "What is the name of your childhood friend?"
        )
    
    class AccountStatus(models.TextChoices):
        ACTIVE = (
            "active",
            _("Active")
        )
        LOCKED = (
            "locked",
            _("Locked")
        )
    
    class RoleChoices(models.TextChoices):
        ADMIN = (
            "admin",
            _("Admin")
        )
        CUSTOMER = (
            "customer",
            _("Customer")
        )
        ACCOUNT_EXECUTIVE = (
            "account_executive",
            _("Account Executive")
        )
        TELLER = (
            "teller",
            _("Teller")
        )
        BRANCH_MANAGER = (
            "branch_manager",
            _("Branch Manager")
        )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    username = models.CharField(
        _("Username"), 
        max_length=15,
        unique=True
    )
    security_question = models.CharField(
        _("Security Question"),
        max_length=50,
        choices=SecurityQuestions.choices,
        default=SecurityQuestions.MAIDEN_NAME
    )
    security_answer = models.CharField(
        _("Security Answer"),
        max_length=50
    )
    email = models.EmailField(
        _("Email"),
        unique=True, 
        db_index=True,
        max_length=255
    )
    first_name = models.CharField(
        _("First Name"),
        max_length=50
    )
    middle_name = models.CharField(
        _("Middle Name"),
        max_length=50,
        null=True,
        blank=True, 
    )
    last_name = models.CharField(
        _("Last Name"),
        max_length=50
    )
    id_no = models.PositiveIntegerField(
        _("ID Number"),
        unique=True
    )
    account_status = models.CharField(
        _("Account Status"),
        max_length=10,
        choices=AccountStatus.choices,
        default=AccountStatus.ACTIVE
    )
    role = models.CharField(
        _("Role"),
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.CUSTOMER
    )
    failed_login_attempts = models.PositiveSmallIntegerField(
        _("Failed Login Attempts"),
        default=0
    )
    last_failed_login = models.DateTimeField(
        _("Last Failed Login"),
        null=True,
        blank=True
    )
    otp = models.CharField(
        _("One-Time Password"),
        max_length=6,
        null=True,
        blank=True
    )
    otp_expiy_time = models.DateTimeField(
        _("OTP Expiry Time"),
        null=True,
        blank=True
    )
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name", 
        "last_name", 
        "id_no", 
        "security_question", 
        "security_answer"
    ]

    def set_otp(self, otp) -> None:
        self.otp = otp
        self.otp_expiy_time = timezone.now() + settings.OTP_EXPIRATION
        self.save()

    def verify_otp(self, otp) -> bool:
        if (
            self.otp == otp
            and self.otp_expiy_time is not None
            and self.otp_expiy_time > timezone.now()
        ):
            self.otp = ""
            self.otp_expiy_time = None
            self.save()
            return True
        return False