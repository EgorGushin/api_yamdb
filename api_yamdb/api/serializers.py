from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from categories.models import Category, Genre, Title
from rest_framework.validators import UniqueTogetherValidator
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    username = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = User


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
