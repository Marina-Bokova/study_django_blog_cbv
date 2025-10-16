from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from .models import Post, Category, Comment, Rating


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'category', 'status')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdminPage(DjangoMpttAdmin):
    pass


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('post', 'value', 'user', 'ip_address')
