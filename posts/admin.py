from django.contrib import admin
from batchadmin.admin import BatchModelAdmin, CHECKBOX_NAME
from models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'comment_status', 'num_moderation_comments', 'num_comments', 'num_spam_comments', 'published_on', 'created_on')
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('author', 'is_published')
    search_fields = ['title', 'body', 'is_published',]
    exclude = ('author', )
    date_hierarchy = 'published_on'
    save_on_top = True

    fieldsets = (
        (None, {
             'classes': ('wide', ),
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

    def num_moderation_comments(self, obj):
        return obj.comments.filter(awaiting_moderation=True).count()
    num_moderation_comments.short_description = 'Awaiting Moderation'
	
    def num_comments(self, obj):
        return obj.comments.filter(is_approved=True).count()
    num_comments.short_description = 'Comments'

    def num_spam_comments(self, obj):
        return obj.comments.filter(is_spam=True).count()
    num_spam_comments.short_description = 'SPAM'
	
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

class CommentAdmin(BatchModelAdmin):
    list_display = ('author_name', 'author_email', 'author_url', 'is_approved', 'is_spam', 'added_on', )
    list_filter = ('awaiting_moderation', 'is_approved', 'is_spam', 'author_name')
    search_fileds = [ 'author_name', 'author_email', 'author_url', 'body' ]
    date_hierarchy = 'added_on'
    save_on_top = True
    
    fieldsets = (
        (None, {
             'classes': ('wide', ),
            'fields': ('author_name', 'author_email', 'author_url', 'body')
        }),
        ('Meta', {
             'classes': ('wide', ),
            'fields': ('author_ip', 'author_user_agent', 'author_referrer')
        }),
        ('Options', {
            'fields': ('awaiting_moderation', 'is_spam', 'is_approved')
        }),
    )

    batch_actions = ['delete_selected', 'mark_list_as_spam', 'approve_list']

    def mark_list_as_spam(self, request, changelist):
        selected = request.POST.getlist(CHECKBOX_NAME)
        objects = changelist.get_query_set().filter(pk__in=selected)
        for obj in objects:
            obj.mark_spam()
        self.message_user(request, "Marked SPAM")

    mark_list_as_spam.short_description = "Mark selected as SPAM"

    def approve_list(self, request, changelist):
        selected = request.POST.getlist(CHECKBOX_NAME)
        objects = changelist.get_query_set().filter(pk__in=selected)
        for obj in objects:
            obj.mark_approved()
        self.message_user(request, "Approved")

    approve_list.short_description = "Approve selected"

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
