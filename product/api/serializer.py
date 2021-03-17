from rest_framework.serializers import ModelSerializer

from product.models import Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'store')



class StoreCategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'store')
        extra_kwargs = {
            'id': {'read_only': True},
        }
