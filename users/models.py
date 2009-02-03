from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class Profile(models.Model):
	"""
	Profile

	Used for keeping track of user settings
	"""
	user = models.ForeignKey(User, unique=True)
	show_email = models.BooleanField(default=False)

	@models.permalink
	def get_absolute_url(self):
		return ('view_profile', [self.user.username])

def auto_create_profile(sender, created, instance, **kwargs):
	"""
	Auto Create Profile

	Uses post_save signal from User model to create profiles for new users
	"""
	if created == True:
		Profile.objects.create(user=instance)

post_save.connect(auto_create_profile, sender=User)
