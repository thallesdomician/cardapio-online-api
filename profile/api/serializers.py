from rest_framework.serializers import ModelSerializer

from profile.models import Profile

from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'is_active')
        extra_kwargs = {
            'username': {'read_only': True},
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True},
            'is_superuser': {'read_only': True},
        }




class ProfileSerializer(ModelSerializer):
    user = UserSerializer()

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')

        user = instance.user

        instance.image = validated_data.get('image', instance.image)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.phone = validated_data.get('phone', instance.phone)

        instance.save()

        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)

        user.save()

        return instance

    class Meta:
        model = Profile
        fields = ('user', 'image', 'birth_date', 'phone', 'created_at', 'updated_at', 'active')
        extra_kwargs = {
            'active': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }


