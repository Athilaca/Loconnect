from django.urls import path
from . views import *

urlpatterns = [
    path('send_otp', SendOTPView.as_view()),
    path('verify_otp', VerifyOTPView.as_view()),
    path('services',ServiceView.as_view()),
    path('category',CategoryView.as_view()),
    path('upload_image/<int:id>/', ServiceImageView.as_view())

]
