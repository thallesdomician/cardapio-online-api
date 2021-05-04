from rest_framework.serializers import ModelSerializer

from address.models import Address, State, City


class StateSerializer(ModelSerializer):
	class Meta:
		model = State
		fields = ( 'name', 'uf')


class CitySerializer(ModelSerializer):
	state = StateSerializer()

	class Meta:
		model = City
		fields = ('name', 'state')



class AddressSerializer(ModelSerializer):
	city = CitySerializer()
	class Meta:
		model = Address
		fields = ('cep', 'id', 'place', 'number', 'complement', 'district', 'city', )

		extra_kwargs = {
			'id': {'read_only': True},
		}

