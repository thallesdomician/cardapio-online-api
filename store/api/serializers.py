from guardian.shortcuts import assign_perm
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import PermissionDenied

from cardapioOnlineApi.settings import PERMISSIONS
from store.models import Store, Phone, StorePlan, OpenTime, OpenDay
from store.validators import valite_cnpj


class OpenTimeSerializer(ModelSerializer):
    class Meta:
        model = OpenTime
        fields = ('start', 'end')


class OpenDaySerializer(ModelSerializer):
    times = OpenTimeSerializer(many=True)

    class Meta:
        model = OpenDay
        fields = ('day_of_week', 'times')

        def validate(self, attrs):
            pass


class PhoneSerializer(ModelSerializer):
    class Meta:
        model = Phone
        fields = ('ddd', 'number', 'main')


class StorePlanSerializer(ModelSerializer):
    class Meta:
        model = StorePlan
        fields = ('plan', 'expiration')


class StoreSerializer(ModelSerializer):

    class Meta:
        model = Store
        fields = (
            'id', 'name', 'logo', 'slug', 'cnpj', 'active', 'created_at', 'updated_at')
        extra_kwargs = {
            'active': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
    def create(self, validated_data):
        store = Store(**validated_data)
        store.save()
        user = self.context['request'].user
        assign_perm('change_store', user, store)
        assign_perm('change_store', user, store)
        assign_perm('change_store', user, store)
        assign_perm('change_store', user, store)

        return store


    def update(self, instance, validated_data):
        user = self.context['request'].user
        if not user.has_perm('store.change_store', instance):
            raise PermissionDenied({"message": "You don't have permission to access",
                                    "object_id": instance.id})
        instance.name = validated_data.get('name', instance.name)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.description = validated_data.get('description', instance.description)
        instance.cnpj = validated_data.get('cnpj', instance.cnpj)

        instance.save()
        return instance
        
    def validate(self, attrs):
        valite_cnpj(attrs['cnpj'])
        UniqueValidator(queryset=Store.objects.all())
        return attrs
