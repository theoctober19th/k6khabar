from django.contrib import admin

from .models import PostModel, CommentModel, CategoryModel

# Register your models here.

admin.site.register(PostModel)
admin.site.register(CommentModel)
admin.site.register(CategoryModel)