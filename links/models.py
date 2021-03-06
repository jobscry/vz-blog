# -*- mode: python; coding: utf-8; -*-
from django.contrib.auth.models import User
from django.db import models
from tagging.fields import TagField

class Link(models.Model):
    """
    Link
    
    Link model for linkroll
    """
    class Meta:
        ordering = ['title', ]
    title = models.CharField(max_length=255)
    url = models.URLField(verify_exists=False)
    extra = models.CharField(max_length=100, default='', blank=True, null=True)
    tags = TagField()
    added_by = models.ForeignKey(User)
    changed_on = models.DateTimeField(blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)
