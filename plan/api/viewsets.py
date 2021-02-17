from rest_framework.viewsets import ModelViewSet

from address.api.serializers import AddressSerializer
from address.models import Address


class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()

    serializer_class = AddressSerializer

