from django import forms
from .models import Post, Categories, Comment

choices=Categories.objects.all().values().values_list('name','name')
choice_list=[]

for item in choices:
	choice_list.append(item)


class PostForm(forms.ModelForm):
	class Meta:
		model=Post
		fields=('title','author','category','body','header_image','snippet')

		widgets={
			'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Title'}),
			'author':forms.TextInput(attrs={'class':'form-control','id':'author_name','value':'','type':'hidden'}),

			# 'author':forms.Select(attrs={'class':'form-control'}),
			'category':forms.Select(choices=choice_list,attrs={'class':'form-control'}),
			'body':forms.Textarea(attrs={'class':'form-control','placeholder':'Enter Body'}),
			'snippet':forms.Textarea(attrs={'class':'form-control','placeholder':'Type your snippet here','rows':2}),


		}

class AddCommentForm(forms.ModelForm):
	class Meta:
		model=Comment 
		fields=('name','body')

class EditForm(forms.ModelForm):
	class Meta:
		model=Post
		fields=('title','category','body','snippet')

		widgets={
			'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Title'}),
			# 'author':forms.Select(attrs={'class':'form-control'}),
			'category':forms.Select(choices=choice_list,attrs={'class':'form-control'}),

			'body':forms.Textarea(attrs={'class':'form-control','placeholder':'Enter Body'}),
			'snippet':forms.Textarea(attrs={'class':'form-control','placeholder':'Type your snippet here','rows':2}),
			

		}


class CategoryForm(forms.ModelForm):
	class Meta:
		model=Categories
		fields='__all__'

		widgets={
			'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter name of category'}),

		}