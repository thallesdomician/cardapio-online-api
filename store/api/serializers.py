from guardian.shortcuts import assign_perm
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import ModelSerializer, ImageField
from rest_framework.validators import UniqueValidator

from address.api.serializers import AddressSerializer
from product.models import Category
from store.models import Store, Phone, StorePlan, OpenTime, OpenDay, StoreAvatar, StoreWallpaper
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
        fields = ('id', 'ddd', 'number', 'main')
        extra_kwargs = {
            'id': {'read_only': True},
        }


class PhoneSerializerList(ModelSerializer):
    phones = PhoneSerializer(many=True)

    class Meta:
        model = Store
        fields = ('id', 'phones',)
        extra_kwargs = {
            'id': {'read_only': True},
        }


class StorePlanSerializer(ModelSerializer):
    class Meta:
        model = StorePlan
        fields = ('plan', 'expiration')


class StoreAvatarSerializer(ModelSerializer):
    avatar = ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = StoreAvatar
        fields = ('avatar', 'id')
        extra_kwargs = {
            'id' : {'read_only': True},
            'url': {'lookup_field': 'id'},
        }

    # def create(self, validated_data):
    #     avatar = StoreAvatar.objects.create(**validated_data)
    #     return avatar
    # super(StoreAvatarSerializer).create(self, validated_data)

    def validate(self, attrs):
        UniqueValidator(queryset=Store.objects.all())
        return attrs


class StoreWallpaperSerializer(ModelSerializer):
    class Meta:
        model = StoreWallpaper
        fields = ('wallpaper', 'id')
        extra_kwargs = {
            'id': {'read_only': True},
        }


class StoreSerializer(ModelSerializer):
    phones = PhoneSerializer(many=True, read_only=True)
    days = OpenDaySerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)
    avatar = StoreAvatarSerializer(required=False, read_only=False)
    wallpaper = StoreWallpaperSerializer(required=False, read_only=False)

    class Meta:
        model = Store
        fields = (
            'id', 'name', 'logo', 'wallpaper', 'avatar', 'slug', 'description', 'cnpj', 'address', 'phones', 'days',
            'active',)
        extra_kwargs = {
            'id'       : {'read_only': True},
            'logo'     : {'read_only': True},
            'wallpaper': {'read_only': True},
            'avatar'   : {'read_only': True},
            'url'      : {'lookup_field': 'slug'},
        }

    def create(self, validated_data):
        user = self.context['request'].user
        # user_stores = list(get_objects_for_user(user, 'store.change_store'))
        # if(len(user_stores) >= 1):
        #     raise PermissionDenied({"message": _("Limit to create stores exceeded.")})

        avatar_data = validated_data.pop('avatar', None)
        wallpaper_data = validated_data.pop('wallpaper', None)
        store = Store(**validated_data)
        store.save()

        if avatar_data:
            StoreAvatar.objects.create(store=store, **avatar_data)
        if wallpaper_data:
            StoreWallpaper.objects.create(store=store, **wallpaper_data)
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

        # avatar_data = validated_data.pop('avatar', None)
        # wallpaper_data = validated_data.pop('wallpaper', None)
        #
        # if avatar_data and avatar_data.get('avatar'):
        #     avatar = instance.avatar
        #     avatar.delete()
        #     StoreAvatar.objects.create(store=instance, **avatar_data)
        # if wallpaper_data and wallpaper_data.get('wallpaper'):
        #     wallpaper = instance.wallpaper
        #     wallpaper.delete()
        #     StoreWallpaper.objects.create(store=instance, **wallpaper_data)

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


class StoreLogoSerializer(ModelSerializer):
    # logo = SerializerMethodField('get_thumbnail_url')

    class Meta:
        model = Store
        fields = ('id', 'logo',)
        extra_kwargs = {
            'id': {'read_only': True},
        }
