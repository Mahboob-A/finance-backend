from typing import Any

from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm 
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _



from .models import User

class UserCreationForm(DjangoUserCreationForm):
    class Meta: 
        model = User 
        fields = [
            "email", 
            "id_no", 
            "first_name",
            "last_name",
            "security_question",
            "security_answer",
            "is_staff", 
            "is_superuser"
        ]

    def clean_email(self) -> str:
        email = self.cleaned_data.get("email")
        if email is None:
            raise ValidationError(_("Email is required."))
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("A user with that email already exists."))
        return email 

    def clean_id_no(self) -> str:
        id_no = self.cleaned_data.get("id_no")
        if id_no is None:
            raise ValidationError(_("ID number is required."))
        if User.objects.filter(id_no=id_no).exists():
            raise ValidationError(_("A user with that ID number already exists."))
        return id_no

    def clean(self) -> dict: 
        cleaned_data = super().clean()
        security_question = cleaned_data.get("security_question")
        security_answer = cleaned_data.get("security_answer")
        is_superuser = cleaned_data.get("is_superuser")

        if not is_superuser: 
            if not security_question: 
                self.add_error("security_question", _("Security question is required for non-superusers."))
            if not security_answer:
                self.add_error("security_answer", _("Security answer is required for non-superusers."))


        return cleaned_data

    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)
        if commit: 
            user.save()
        return user


class UserChangeForm(DjangoUserChangeForm):
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "id_no",
            "security_question",
            "security_answer",
            "is_staff",
            "is_superuser", 
            "is_active"
        ]
    def clean_email(self) -> str:
        email = self.cleaned_data.get("email")
        if email is None:
            raise ValidationError(_("Email is required."))
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError(_("A user with that email already exists."))
        return email
    
    def clean_id_no(self) -> str:
        id_no = self.cleaned_data.get("id_no")
        if id_no is None:
            raise ValidationError(_("ID number is required."))
        if User.objects.exclude(pk=self.instance.pk).filter(id_no=id_no).exists():
            raise ValidationError(_("A user with that ID number already exists."))
        return id_no
    
    def clean(self) -> dict: 
        cleaned_data = super().clean()
        security_question = cleaned_data.get("security_question")
        security_answer = cleaned_data.get("security_answer")
        is_superuser = cleaned_data.get("is_superuser")

        if not is_superuser: 
            if not security_question: 
                self.add_error("security_question", _("Security question is required for non-superusers."))
            if not security_answer:
                self.add_error("security_answer", _("Security answer is required for non-superusers."))


        return cleaned_data