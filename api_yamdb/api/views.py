import random
import string

from django.core.mail import send_mail
from django.db.models import Avg, F
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter
from .models import Category, Comment, Genre, Review, Title, User
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAuthorModeratorAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          EmailSerializer, GenreSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          TokenSerializer, UserSerializer)


class CreateListViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    pass


def generate_username_from_email(email):
    username = email.split('@')[0]
    if User.objects.filter(username=username).exists():
        return email
    return username


def generate_confirmation_code():
    return ''.join(
        [random.choice(
            string.ascii_letters + string.digits
        ) for n in range(8)])


class SendConfirmationCode(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        confirmation_code = generate_confirmation_code()
        User.objects.create(
            email=email, confirmation_code=confirmation_code,
            username=generate_username_from_email(email),
            is_active=False
        )
        send_mail(
            'Код подтверждения Yamdb',
            f'Ваш код подтверждения: {confirmation_code}',
            'admin@yamdb.ru',
            [email]
        )
        return Response(
            'Код подтверждения успешно отправлен!',
            status=status.HTTP_200_OK
        )


class SendJwtToken(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        confirmation_code = serializer.validated_data.get(
            'confirmation_code'
        )
        if not User.objects.filter(
            email=email, confirmation_code=confirmation_code
        ).exists():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.get(
            email=email, confirmation_code=confirmation_code
        )
        user.is_active = True
        user.save()
        token = AccessToken.for_user(user)
        return Response(
            f'token: {token}', status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]
    pagination_class = PageNumberPagination


class UserMe(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                'Вам нужно авторизоваться!',
                status=status.HTTP_401_UNAUTHORIZED
            )
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        if not request.user.is_authenticated:
            return Response(
                'Вам нужно авторизоваться!',
                status=status.HTTP_401_UNAUTHORIZED
            )
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


class GenreViewSet(CreateListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ('name',)


class CategoryViewSet(CreateListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filterset_class = TitleFilter

    def get_queryset(self):
        return super().get_queryset().annotate(
            rating=Avg(F('reviews__score'))).order_by('year')

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleWriteSerializer
        return TitleReadSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthorModeratorAdminOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthorModeratorAdminOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        queryset = Comment.objects.filter(review=review, title=title)
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, review=review, title=title)
