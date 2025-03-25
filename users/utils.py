from django.core.mail import send_mail
from .models import EmailVerificationCode
import random


def generate_code():
    return str(random.randint(100000, 999999))


def send_verification_code(email):
    code = generate_code()
    EmailVerificationCode.objects.create(email=email, code=code)

    send_mail(
        "Ваш код подтверждения",
        f"Ваш код подтверждения: {code}",
        "odilbek.arziev@yandex.ru",
        [email],
        fail_silently=False,
    )
