from django.contrib import admin
from posts.models import Post
from posts.forms import PostAdminForm

class PostAdmin(admin.ModelAdmin):
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
        ('Comment Options', {
            'fields': ('comments_enabled', 'override_max_comment_age')
        }),
        ('Publishing Options', {
            'fields': ('is_published', 'published_on', 'update_pingbacks')
        }),
    )

    def comment_status(self, obj):
        if obj.can_comment():
            return 'open'
        return 'closed'

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

admin.site.register(Post, PostAdmin)
