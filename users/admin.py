from django.contrib import admin
from .models import *

admin.site.register(EmailVerificationCode)
admin.site.register(User)
