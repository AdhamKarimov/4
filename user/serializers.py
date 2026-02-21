from rest_framework import serializers, status
from .models import CustomUser
from rest_framework.exceptions import ValidationError


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    conf_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'password',
                  'conf_password']

    def validate(self, data):
        password = data.get('password', None)
        conf_password = data.get('conf_password', None)

        if password is None or conf_password is None or password != conf_password:
            response = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Parollar mos emas yoki xato kiritildi'
            }
            raise ValidationError(response)
        if len([i for i in password if i == ' ']) > 0:
            response = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Parollar xato kiritildi'
            }
            raise ValidationError(response)

        return data

    def validate_username(self, username):
        if len(username) < 6:
            raise ValidationError({'message': 'Username kamida 7 ta bolishi kerak'})
        elif not username.isalnum():
            raise ValidationError({'message': 'Username da ortiqcha belgilar bolmasligi kerak'})
        elif username[0].isdigit():
            raise ValidationError({'message': 'Username raqam bilan boshlanmasin'})
        return username

    def create(self, validated_data):
        validated_data.pop('conf_password')

        user = CustomUser.objects.create_user(
            **validated_data
        )

        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class ProfilUdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','last_name', 'first_name', 'email', 'phone_number', 'address',]

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)

        instance.save()
        return instance


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    conf_password = serializers.CharField(required=True)

    def validate(self, data):
        new_password = data.get('new_password', None)
        conf_password = data.get('conf_password', None)

        if new_password is None or conf_password is None or new_password != conf_password:
            response = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Parollar mos emas yoki xato kiritildi'
            }
            raise ValidationError(response)
        if len([i for i in new_password if i == ' ']) > 0:
            response = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Parollar xato kiritildi'
            }
            raise ValidationError(response)

        return data
