from django.core.files import File
from django.contrib.auth.modles import User
from django.db import models

class Attachment(models.Model):
    """
    Attachment model
    """
    name = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User)
    uploaded_on = models.DateTimeField(auto_now_add=True)

class Archive(Attachement):
    """
    Files
    """

class Image(Attachment):
    
