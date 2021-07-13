import django_filters.rest_framework
from rest_framework import filters, mixins, viewsets

from .serializers import GenreSerializer, CategorySerializer, TitleSerializer
from .models import Genre, Category, Title


class CreateListViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet,
                        mixins.DestroyModelMixin):
    pass


class GenreViewSet(CreateListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]

    search_fields = ['name', ]


class CategoryViewSet(CreateListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ['name', ]


# class TitleViewSet(viewsets.ModelViewSet):
#     queryset = Title.objects.all()
#     serializer_class = TitleSerializer
#     filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
#     filterset_fields = ['genre', 'category', ]

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)
