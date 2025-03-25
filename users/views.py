from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse

from store.models import *
from .utils import send_verification_code
from .models import EmailVerificationCode
from .forms import *


def sign_out(request):
    logout(request)
    return redirect('store:home')


def connect_data(request):
    token = request.COOKIES['csrftoken']
    guest = Guest.objects.filter(token=token)
    cart_items = CartItem.objects.filter(guest=guest[0]) if guest else []

    for item in cart_items:
        item.customer = request.user
        item.guest = None
        item.save()
    guest.delete()


def edit_profile(request):
    form = EditProfileForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('store:home')
    return render(request, 'edit_profile.html', {'form': form})


def reset_password(request):
    form = ResetPasswordForm(request.user, request.POST or None)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        return redirect('users:sign_in')
    return render(request, 'reset_password.html', {'form': form})


def request_code(request):
    form = EmailForm(request.POST or None)

    if form.is_valid():
        email = form.cleaned_data['email']

        send_verification_code(email)
        return redirect('users:verify_code', email=email)

    return render(request, 'request_code.html', {'form': form})


def verify_code(request, email):
    form = AuthForm(request.POST or None)

    if form.is_valid():
        code = form.cleaned_data['code']
        verification = EmailVerificationCode.objects.filter(email=email, code=code).last()

        if not verification or verification.is_expired():
            return JsonResponse({"error": "Incorrect or expired code"}, status=400)

        user, created = User.objects.get_or_create(email=email)

        # Важно: передаём backend явно
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        EmailVerificationCode.objects.filter(email=email).delete()
        return redirect('store:home')
    return render(request, 'verify_code.html', {'form': form})
