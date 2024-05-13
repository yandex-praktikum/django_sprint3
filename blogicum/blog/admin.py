from django.contrib import admin
from .models import Category, Location, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'text', 'category',
                    'location', 'pub_date', 'created_at', 'is_published')
    search_fields = ('text', )
    list_display_links = ('title', )
    list_editable = ('category', 'is_published', 'location')
    list_filter = ('created_at', )


class PostInLine(admin.StackedInline):
    model = Post
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = (PostInLine, )
    list_display = ('id', 'title', 'description', 'slug', 'created_at')
    list_display_links = ('title', )
    search_fields = ('text', )
    list_filter = ('created_at', )


class LocationAdmin(admin.ModelAdmin):
    inlines = (PostInLine, )
    list_display = ('id', 'name', 'is_published', 'created_at')
    list_display_links = ('name', )
    search_fields = ('text', )
    list_filter = ('created_at', )


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
empty_value_display = 'не задано'
