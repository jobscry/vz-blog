from django.contrib import admin
from django.forms.models import modelformset_factory
from models import Post, Comment, CommentsToPosts

class CommentsToPostsInline(admin.TabularInline):
    model = CommentsToPosts
    extra = 1
    template = 'admin-comments.html'

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'num_comments', 'published_on', 'created_on')
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('author', 'is_published')
    search_fields = ['title', 'body', 'is_published',]
    exclude = ('author', )
    date_hierarchy = 'published_on'
    save_on_top = True
    inlines = [ CommentsToPostsInline, ]

    fieldsets = (
        (None, {
             'classes': ('wide', ),
            'fields': ('title', 'slug', 'tags', 'body')
        }),
        ('Publishing ptions', {
            'fields': ('is_published', 'published_on', 'update_pingbacks')
        }),
    )
	
    def num_comments(self, obj):
        return obj.comments.filter(is_approved=True).count()
    num_comments.short_description = 'Comments'
	
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
