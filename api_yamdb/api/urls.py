from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, SendConfirmationCode, SendJwtToken,
                    TitleViewSet, UserMe, UserViewSet)

router_v1 = DefaultRouter()
router_v1.register(
    'titles',
    TitleViewSet, basename='title'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment'
)
router_v1.register(
    'users',
    UserViewSet, basename='user'
)
router_v1.register(
    'genres',
    GenreViewSet, basename='genre'
)
router_v1.register(
    'categories',
    CategoryViewSet, basename='category'
)

auth_patterns = [
    path('email/', SendConfirmationCode.as_view()),
    path('token/', SendJwtToken.as_view()),
]

urlpatterns = [
    path('v1/users/me/', UserMe.as_view()),
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_patterns)),
]
