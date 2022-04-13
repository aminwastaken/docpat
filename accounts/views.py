from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import AddressForm, CustomUserCreationForm, CustomUserLoginForm
from django.contrib.auth import authenticate, login, logout


# class SignUpView(CreateView):
#     form_class = CustomUserCreationForm
#     form2_class = AddressForm
#     success_url = reverse_lazy("login")
#     template_name = "signup.html"

def SignupView2(request):
    if request.method == 'POST':
        form1 = CustomUserCreationForm(request.POST)
        form2 = AddressForm(request.POST)
        if all((form1.is_valid(), form2.is_valid())):
            user = form1.save()
            address = form2.save(commit=False)
            address.user = user
            address.save()
            return HttpResponseRedirect(reverse_lazy("login"))

# if a GET (or any other method) we'll create a blank form
    else:
        form1 = CustomUserCreationForm()
        form2 = AddressForm()

    return render(request, 'signup2.html', {'form1': form1,'form2': form2})


# class LoginView(CreateView):
#     form_class = CustomUserLoginForm
#     success_url = reverse_lazy("login")
#     template_name = "login.html"


class LoginView(TemplateView):

    template_name = 'login.html'

    success_url = reverse_lazy("login")

    def get(self, request, **kwargs):
        form_class = CustomUserLoginForm
        if request.user.is_authenticated:
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name)

    def post(self, request, **kwargs):

        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

        return render(request, self.template_name)
