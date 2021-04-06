import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from profile.api.serializers import ProfileSerializer
from profile.models import Profile


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {
            "username": "testcase",
            "email": "testcase@testcase.com",
            "password": "!Q@W3e4r",
            "first_name": "Test",
            "last_name": "Case",
            "password2": "!Q@W3e4r",
        }

        response = self.client.post("/auth/register/", data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)