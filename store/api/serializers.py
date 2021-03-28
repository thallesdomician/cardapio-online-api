from guardian.shortcuts import assign_perm
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from address.api.serializers import AddressSerializer
from product.models import Category
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
	phones = PhoneSerializer(many=True, read_only=True)
	days = OpenDaySerializer(many=True, read_only=True)
	address = AddressSerializer(read_only=True)

	class Meta:
		model = Store
		fields = ('id', 'name', 'logo', 'slug', 'description', 'cnpj', 'address', 'phones', 'days', 'active',)
		extra_kwargs = {
			'id'    : {'read_only': True},
			'logo'  : {'read_only': True},
			'url'   : {'lookup_field': 'slug'},
		}

	def create(self, validated_data):
		user = self.context['request'].user
		# user_stores = list(get_objects_for_user(user, 'store.change_store'))
		# if(len(user_stores) >= 1):
		#     raise PermissionDenied({"message": _("Limit to create stores exceeded.")})

		store = Store(**validated_data)
		store.save()
		assign_perm('store.change_store', user, store)
		assign_perm('store.delete_store', user, store)

		return store

	def update(self, instance, validated_data):
		user = self.context['request'].user
		if not user.has_perm('store.change_store', instance):
			raise PermissionDenied({"message"  : "You don't have permission to access",
			                        "object_id": instance.id})
		instance.name = validated_data.get('name', instance.name)
		instance.slug = validated_data.get('slug', instance.slug)
		instance.description = validated_data.get('description', instance.description)
		instance.cnpj = validated_data.get('cnpj', instance.cnpj)

		instance.save()
		return instance

	def validate(self, attrs):
		valite_cnpj(attrs['cnpj'])
		UniqueValidator(queryset=Store.objects.all())
		return attrs


class StoreCategorySerializer(ModelSerializer):
	class Meta:
		model = Category
		fields = ('name',)
