from rest_framework import serializers

from users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'tg_username', 'tg_id', 'password')
        extra_kwargs = {
                'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            tg_username=validated_data['tg_username'],
            tg_id=validated_data['tg_id'],
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
