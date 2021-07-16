from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'bio', 'role', 'confirmation_code')


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'year', 'description')
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'score', 'pub_date', 'title')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'pub_date', 'title', 'review')
    empty_value_display = '-пусто-'
