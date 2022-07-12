from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from rest_framework import filters, viewsets

from categories.models import Category, Genre, Title
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer, UserSerializer)
from users.models import User

from rest_framework.permissions import IsAuthenticatedOrReadOnly, \
    IsAuthenticated
from .permissions import *
                          

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    )
    filter_backend = (SearchFilter, )
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    )
    filter_backend = (SearchFilter, )
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    )
    filter_backend = (DjangoFilterBackend, )
    filterset_fields = ('category', 'genre', 'name', 'year')
    
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin
    )
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('username', )
    lookup_field = 'username'
    # pagination_class = LimitOffsetPagination
