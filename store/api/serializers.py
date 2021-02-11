from rest_framework.fields import SlugField
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from store.models import Store
from store.validators import valite_cnpj

class StoreSerializer(ModelSerializer):
    # slug = SlugField(
    #     max_length=150,
    #     validators=[UniqueValidator(queryset=Store.objects.all())]
    # )
    class Meta:
        model = Store
        fields = ('id', 'name', 'slug', 'cnpj', 'full_address', 'specialty', 'active', 'created_at', 'updated_at')

        def validate(self, attrs):
            valite_cnpj(attrs['cnpj'])
            UniqueValidator(queryset=Store.objects.all())


