from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.generic import TemplateView


class AboutPage(TemplateView):
    template_name = 'pages/about.html'


class RulesPage(TemplateView):
    template_name = 'pages/rules.html'


class RegistrationSuccessPage(TemplateView):
    template_name = 'registration/registration_success.html'


@login_required
def user_logout(request):
    logout(request)
    return render(request, 'registration/logged_out.html')
