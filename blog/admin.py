from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from blog.models import Post, Commentary, User


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    list_filter = ("created_time",)
    list_display = (
        "author",
        "title",
        "content",
    )


@admin.register(Commentary)
class CommentaryAdmin(admin.ModelAdmin):
    search_fields = ("content",)
    list_filter = ("created_time",)
    list_display = (
        "author",
        "post",
        "content",
        "created_time",
    )


@admin.register(User)
class UserAdmin(UserAdmin):
    search_fields = ("username",)
    list_filter = ("is_staff",)


admin.site.unregister(Group)
