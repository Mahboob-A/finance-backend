import random
import string


def generate_otp(length=6) -> str:
    """Generate a random OTP of specified length."""

    characters = string.digits
    otp = ''.join(random.choices(characters, k=length))
    return otp
