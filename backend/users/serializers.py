from djoser.serializers import UserSerializer

from users.models import User


class CustomUserSerializer(UserSerializer):
    """Сериализатор работы с пользователями."""

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'telegram_id',
            'password'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'telegram_id': {'required': False},
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        if 'telegram_id' in validated_data:
            user.telegram = validated_data['telegram']

        user.set_password(validated_data['password'])
        user.save()
        return user
