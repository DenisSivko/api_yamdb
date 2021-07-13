from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from .views import ...

router_v1 = DefaultRouter()
router_v1.register(r'titles', "VIEW-ФУНКЦИЯ", basename='titles')
router_v1.register(r'titles/(?P<title_id>\d+)', "VIEW-ФУНКЦИЯ",
                   basename='title_detail')
router_v1.register(r'/titles/(?P<title_id>\d+)/reviews/', "VIEW-ФУНКЦИЯ",
                   basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)',
                   "VIEW-ФУНКЦИЯ", basename='review_comments')
router_v1.register(r'users',
                   "VIEW-ФУНКЦИЯ", basename='users')
router_v1.register(r'genres',
                   "VIEW-ФУНКЦИЯ", basename='genres')
router_v1.register(r'categories',
                   "VIEW-ФУНКЦИЯ", basename='categories')
urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
