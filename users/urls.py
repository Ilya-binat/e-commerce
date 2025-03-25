from django.urls import path, include
from . import views

urlpatterns = [
    path("auth/request-code/", views.request_code, name="request_code"),
    path("auth/verify-code/<str:email>", views.verify_code, name="verify_code"),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('reset_password/', views.reset_password, name='reset_password'),
]
