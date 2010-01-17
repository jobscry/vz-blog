# -*- mode: python; coding: utf-8; -*-
from django.contrib import admin
from django.contrib.contenttypes import generic
from models import Link

class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'added_by', 'changed_on', 'added_on')
    search_fields = ['title', 'ulr',]
    exclude = ('added_by',)
    date_hierarchy = 'added_on'
	
    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        obj.save()

admin.site.register(Link, LinkAdmin)
