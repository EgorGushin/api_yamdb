from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
# from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser

from users.models import User
# from .permissions import UserIsAuthor
from .serializers import (
    # CommentSerializer,
    # FollowSerializer,
    # GroupSerializer,
    # PostSerializer,
    UserSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('username', )
    lookup_field = 'username'
    # pagination_class = LimitOffsetPagination
