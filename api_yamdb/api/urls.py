from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GenreViewSet, CategoryViewSet

router_v1 = DefaultRouter()
#router_v1.register(r'titles', TitleViewSet, basename='titles')
#router_v1.register(r'/titles/(?P<title_id>\d+)/reviews/', "VIEW-ФУНКЦИЯ",
                  # basename='reviews')
#router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)',
                   #"VIEW-ФУНКЦИЯ", basename='review_comments')
#router_v1.register(r'users',
                  # "VIEW-ФУНКЦИЯ", basename='users')
router_v1.register(r'genres',
                   GenreViewSet, basename='genres')
router_v1.register(r'categories',
                   CategoryViewSet, basename='categories')
urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
