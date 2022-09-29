from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class PasswordResetView(PasswordResetView):
    send_mail('Тема письма',
              'Текст письма.',
              'from@example.com',
              ['to@example.com'],
              fail_silently=False,
              )
