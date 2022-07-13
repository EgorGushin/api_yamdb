from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from categories.models import Category, Genre, Title
from reviews.models import Comment, Review
from users.models import User
from users.validators import validate_username


# User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=(UniqueValidator(queryset=User.objects.all()), ),
        required=True
    )
    email = serializers.EmailField(
        validators=(UniqueValidator(queryset=User.objects.all()), ),
    )

    class Meta:
        fields = '__all__'
        model = User


class GetConfirmationCodeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=(UniqueValidator(queryset=User.objects.all()), )
    )
    email = serializers.EmailField(
        validators=(UniqueValidator(queryset=User.objects.all()), )
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать никнейм "me" запрещено.'
            )
        return value

    class Meta:
        model = User
        fields = ('username', 'email')


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )

    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'
