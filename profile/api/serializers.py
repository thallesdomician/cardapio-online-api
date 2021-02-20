from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

from django.core import exceptions
import django.contrib.auth.password_validation as validators
from rest_framework import serializers


from profile.models import Profile

class UserRegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','username', 'password')

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()
        Profile.objects.create(user=user, active=False)
        return user

    def validate(self, data):
        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        user = User(**data)

        # get the password from the data
        password = data.get('password')

        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=User)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserRegisterSerializer, self).validate(data)


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


