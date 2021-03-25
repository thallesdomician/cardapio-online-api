from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from profile.api.serializers import UserSerializer
from profile.forms import CreateForm, ProfileUpdateForm, AuthenticationProfileForm
from profile.models import Profile


class ProfileDetail(ListView):
    model = Profile

class ProfileCreate(CreateView):
    model = User
    form_class = CreateForm

    def get_success_url(self, **kwargs):
        return reverse_lazy("login")

class ProfileDetail(DetailView):
    model = Profile



class ProfileUpdate(UpdateView):
    model = Profile
    template_name_suffix = '_update_form'
    fields = ['image', 'birth_date', 'phone', ]

    def get_success_url(self):
        return reverse('profile_update', kwargs={'pk': self.request.user.id})


class LoginProfileView(LoginView):
    form_class = AuthenticationProfileForm



class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)