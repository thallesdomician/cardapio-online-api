from rest_framework.viewsets import ModelViewSet

from profile.api.serializers import ProfileSerializer
from profile.models import Profile


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer





