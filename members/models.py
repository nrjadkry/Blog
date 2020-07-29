from django.db import models

from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
	user=models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	bio=models.TextField()
	profile_picture=models.ImageField(null=True,blank=True,default='default.jpg', upload_to='images/')

	def __str__(self):
		return str(self.user)
