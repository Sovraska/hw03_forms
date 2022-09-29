from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.mail import send_mail

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


def send_msg(email):

    send_mail('Тема письма',
              'Текст письма.',
              email,
              ['to@example.com'],
              fail_silently=False,
              )
