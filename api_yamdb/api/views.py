from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.filters import SearchFilter

from rest_framework import filters, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from rest_framework import filters, viewsets, pagination

from categories.models import Category, Genre, Title
from reviews.models import Comment, Review
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleSerializer, UserSerializer,
                          GetConfirmationCodeSerializer, GetTokenSerializer)
from users.models import User
from .mixins import ListCreateDestroyViewSet

from rest_framework.permissions import IsAuthenticatedOrReadOnly, \
    IsAuthenticated, AllowAny
from .permissions import *


# User = get_user_model()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = (
    #     IsAuthenticatedOrReadOnly,
    #     IsAdminOrReadOnly
    # )
    # filter_backend = (SearchFilter, )
    # search_fields = ('name',)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = (
    #     IsAuthenticatedOrReadOnly,
    #     IsAdminOrReadOnly
    # )
    # filter_backend = (SearchFilter, )
    # search_fields = ('name',)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (
        IsModerAdminAuthor,
        IsAdminOrReadOnly
    )
    filter_backend = (SearchFilter, )
    search_fields = ('name',)
    lookup_field = "slug"


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    )
    filter_backend = (SearchFilter, )
    search_fields = ('name',)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    )
    filter_backend = (DjangoFilterBackend, )
    filterset_fields = ('name', 'year', 'genre', 'category')


class GetConfirmationCodeView(APIView):
    http_method_names = ('post', )
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = GetConfirmationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        to_email = serializer.validated_data['email']
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Код подтверждения',
            f'Ваш код подтверждения: {confirmation_code}',
            settings.FROM_EMAIL,
            [to_email],
            fail_silently=False,
        )
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class GetTokenApiView(APIView):
    http_method_names = ('post', )
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        if default_token_generator.check_token(user, confirmation_code):
            access_token = RefreshToken.for_user(user).access_token
            data = {'token': str(access_token)}
            return Response(data, status=status.HTTP_201_CREATED)
        errors = {'error': 'Неверный код подтверждения'}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        IsAdmin,
    )
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('username', )
    lookup_field = 'username'
    # pagination_class = LimitOffsetPagination

    @action(
        methods=('get', 'patch'),
        detail=False, url_path='me',
        permission_classes=[
            IsAuthenticated,
        ]
    )
    def get_self_page(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes((AllowAny,))
def sign_up(request):
    serializer = GetConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        User,
        username=serializer.validated_data.get('username')
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Регистрация на сервисе Yamdb',
        message=f'Ваш код подтверждения - {confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=(user.email, )
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data.get('username')
    )
    if default_token_generator.check_token(
        user, serializer.validated_data.get('confirmation_code')
    ):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
