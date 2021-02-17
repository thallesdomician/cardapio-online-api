from rest_framework.serializers import ModelSerializer

from address.models import Address


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'store', 'place', 'number', 'complement', 'district', 'city', 'cep', 'created_at', 'updated_at')