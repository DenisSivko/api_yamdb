from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Genre, Category, Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        lookup_field = 'slug'
        fields = ('name', 'slug', )
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        lookup_field = 'slug'
        fields = ('name', 'slug', )
        model = Category


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title
