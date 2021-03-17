
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .api.serializer import RegisterOwnerSerializer


class RegisterOwnerView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterOwnerSerializer
