from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters

from categories.models import Category, Genre, Title
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer)

class CategoryViewSet():
    queryset = Category.objects.all()
    serializers_class = CategorySerializer
    permission_classes = 
    filter_backend = (filters.SearchFilter)
    search_fields = ('name',)

class GenreViewSet():
    queryset = Genre.objects.all()
    serializers_class = GenreSerializer
    permission_classes = 
    filter_backend = (filters.SearchFilter)
    search_fields = ('name',)

class TitleViewSet():
    queryset = Title.objects.all()
    serializers_class = TitleSerializer
    permission_classes = 
    filter_backend = (DjangoFilterBackend)
    filterset_fields = ('category', 'genre', 'name', 'year')
