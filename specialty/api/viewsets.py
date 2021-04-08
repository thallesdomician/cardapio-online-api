from rest_framework.viewsets import ModelViewSet

from specialty.api.serializers import SpecialtySerializer
from specialty.models import Specialty


class SpecialtyViewSet(ModelViewSet):
    queryset = Specialty.objects.all()

    serializer_class = SpecialtySerializer
