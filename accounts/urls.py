from django.urls import path

from .views import LoginView,SignupView2


urlpatterns = [
    path("signup/", SignupView2, name="signup"),
]
