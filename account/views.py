from django.shortcuts import render
from django.views.generic.edit import FormView, CreateView
from django.core.urlresolvers import reverse_lazy
from account.models import User
from account.forms import UserCreationForm


class UserCreate(CreateView):
    template_name = 'account/create.html'
    form_class = UserCreationForm
    model = User
