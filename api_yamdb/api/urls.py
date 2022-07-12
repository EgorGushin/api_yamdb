from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (
    # CategoryViewSet,
    # CommentViewSet,
    # GenreViewSet,
    # ReviewViewSet,
    # TitleViewSet,
    UserViewSet,
)

router = routers.DefaultRouter()
# router.register('categories', CategoryViewSet, basename='categories')
# router.register('genres', GenreViewSet, basename='genres')
# router.register('titles', TitleViewSet, basename='titles')
# router.register(
#     r'^titles/(?P<title_id>\d+)/reviews',
#     ReviewViewSet,
#     basename='reviews')
# router.register(
#     r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentViewSet,
#     basename='comments')
router.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    # path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path(
        'v1/auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    )
]
