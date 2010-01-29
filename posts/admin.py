# -*- mode: python; coding: utf-8; -*-
from django.contrib import admin
from posts.models import Post
from posts.forms import PostAdminForm

class PostAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': (
                "js/markitup/skins/markitup/style.css",
                "js/markitup/sets/markdown/style.css"
            )
        }
        js = (
            "js/jquery.js",
            "js/markitup/jquery.markitup.pack.js",
            "js/markitup/sets/markdown/set.js"
            "js/markitup.js"
        )

        

    form = PostAdminForm
    list_display = ('title', 'author', 'is_published', 'published_on', 'created_on')
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('author', 'is_published')
    search_fields = ['title', 'body', 'is_published',]
    exclude = ('author', )
    date_hierarchy = 'published_on'
    save_on_top = True

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'tags', 'body')
        }),
        ('Publishing Options', {
            'fields': ('is_published', 'published_on', 'update_pingbacks')
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


admin.site.register(Post, PostAdmin)
