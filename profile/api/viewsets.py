from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.contrib.auth.models import User

from profile.api.serializers import ProfileSerializer, UserSerializer
from profile.models import Profile


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    @action(methods=['get'], detail=False, url_path='user', url_name='profile_user')
    def user(self, request, *args, **kwargs):
        user = request.user
        queryset = User.objects.get(pk=user.pk)

        serializer = UserSerializer(queryset)
        return Response(serializer.data)
