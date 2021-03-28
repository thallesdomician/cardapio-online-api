from rest_framework.serializers import ModelSerializer

from address.models import Address, State, City


class StateSerializer(ModelSerializer):
	class Meta:
		model = State
		fields = ( 'name', 'uf')


class CitySerializer(ModelSerializer):
	state = StateSerializer(read_only=True)

	class Meta:
		model = City
		fields = ('name', 'state')


class AddressSerializer(ModelSerializer):
	city = CitySerializer(read_only=True)
	class Meta:
		model = Address
		fields = ('id', 'store', 'place', 'number', 'complement', 'district', 'city', 'cep')
