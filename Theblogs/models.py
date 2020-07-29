from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from ckeditor.fields import RichTextField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation

class Categories(models.Model):
	name=models.CharField(max_length=30, unique=True)

	def __str__(self):
		return self.name 

	def get_absolute_url(self):
		return reverse('home')

	#This makes all the letters to lowercase in name.
	def save(self, *args, **kwargs):
		self.name = self.name.lower()
		return super(Categories, self).save(*args, **kwargs)
    
    

class Post(models.Model):
	title = models.CharField(max_length=255)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	header_image=models.ImageField(null=True, blank=True, upload_to='images/')
	# category=models.ForeignKey(Categories, on_delete=models.SET_NULL,blank=True, null=True)
	category=models.CharField(max_length=255, default='Sports')
	
	snippet = models.TextField()
	body = RichTextField(blank=True,null=True)	
	published_date=models.DateField(auto_now_add=True)
	likes=models.ManyToManyField(User, related_name='blog_posts')
	blog_views=models.IntegerField(default=0)
	# hit_count_generic=GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')


	def total_likes(self):
		return self.likes.count()

	def __str__(self):
		return self.title + ' by ' + str(self.author)

	def get_absolute_url(self):
		# return reverse('article_detail', args=(str(self.id)))
		return reverse('home')


class Comment(models.Model):
	post = models.ForeignKey(Post,related_name="comments", on_delete=models.CASCADE)
	name=models.CharField(max_length=255)
	body=models.TextField()
	date_added=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '%s - %s' % (self.post.title + ' by '+ str(self.post.author), self.name)

