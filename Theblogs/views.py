from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Categories
from django.views.generic import ListView, DetailView, CreateView,UpdateView, DeleteView
from .forms import PostForm, EditForm, CategoryForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
from hitcount.views import HitCountDetailView
import csv
import xlwt
from django.http import HttpResponse

from .resources import CategoryResource
from django.contrib import messages 
from tablib import Dataset

def import_category(request):
	if request.method=='POST':
		category_resource=CategoryResource()
		dataset=Dataset()
		new_category=request.FILES['myfile']

		# imported_data = dataset.load(new_persons.read(),format='xlsx')

		imported_data=dataset.load(new_category.read(),format='xlsx')
		# result=category_resource.import_data(dataset,dry_run=True)

		# if not result.has_errors():
		# 	result=category_resource.import_data(dataset,dry_run=False)
		# 	print('H')
		# else:
		# 	print('e')


	

		for data in imported_data:
			value=Categories(
				data[0],
				data[1]
				)
			value.save()
	return redirect('categories')

def UserArticleView(request, username):

	queryset = Post.objects.filter(author__username=username).order_by('-published_date')
	return render(request, 'Theblog/user_articles.html', {'articles': queryset})


class HomeView(ListView):
	model = Post
	template_name='Theblog/index.html'
	ordering = ['-id']
	paginate_by=4
	# ordering = ['-published_date']

	def get_context_data(self,*args,**kwargs):
		cat_menu=Categories.objects.all()
		context=super(HomeView,self).get_context_data(*args, **kwargs)

		context['cat_menu']=cat_menu



		return context

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query:
			queryset=[]
			queries=query.split(" ")

			for i in queries: # Thifrom hitcount.views import HitCountDetailViews part removes the word with single letter which makes the search result good.
				if len(i) ==1:
					queries.remove(i)
			if queries:
			
				for q in queries:
					print(q)

					posts = self.model.objects.filter(Q(title__icontains=q) | Q(body__icontains=q) | Q(snippet__icontains=q))
					for post in posts:
						queryset.append(post)
				return list(set(queryset))
			else:
				queryset=self.model.objects.all()

		else:
			queryset=self.model.objects.all()
		return queryset

	    
class CategoryListView(ListView):
	model=Categories
	template_name='Theblog/category_list.html'

	# def get_context_data(request):
	# 	if request.method=='POST':
	# 		category_resource=CategoryResource()
	# 		dataset=Dataset()
	# 		new_category=request.FILES['myfile']

	# 		if not new_category.endswith('xlsx'):
	# 			messages.info(request,'Wrong file format')
	# 			return render(request,'category_list.html')

	# 		imported_data=dataset.load(new_category.read(),format='xlsx')
			
	# 		for data in imported_data:
	# 			value=Post(
	# 				data[0],
	# 				data[1]
	# 				)
	# 			value.save()
	# 	return render(request,'category_list.html')


class ArticleDetailView(HitCountDetailView):
	model = Post
	template_name='Theblog/article_detail.html'

	count_hit=True

	def get_context_data(self,*args,**kwargs):
		cat_menu=Categories.objects.all()
		context=super(ArticleDetailView,self).get_context_data(*args, **kwargs)

		stuff=get_object_or_404(Post,id=self.kwargs['pk'])
		total_likes=stuff.total_likes()

		liked=False
		if stuff.likes.filter(id=self.request.user.id).exists():
			liked=True
			
		context.update({
        'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:3],
        })

		# context['popular_posts']=Post.objects.order_by('hit_count_generic__hits')[:3]

		context['cat_menu']=cat_menu
		context['total_likes']=total_likes
		context['liked']=liked

		return context

	def get_object(self):
		obj=super().get_object()
		obj.blog_views+=1
		obj.save()
		return obj


class CreateBlogView(CreateView):
	model = Post
	form_class=PostForm
	# fields='__all__'
	template_name='Theblog/addblog.html'

class CreateCategoryView(CreateView):
	model = Categories
	form_class=CategoryForm
	# fields='__all__'
	template_name='Theblog/addcategory.html'



class UpdatePostView(UpdateView):
	model=Post
	form_class=EditForm
	template_name='Theblog/updatepost.html'
	# fields=['title','body']

class DeletePostView(DeleteView):
	model=Post
	template_name='Theblog/deletepost.html'
	success_url=reverse_lazy('home')

def CategoryView(request, cate):

	category_post=Post.objects.filter(category=cate.replace('-',' '))
	context={
	'cate':cate.title().replace('-',' '),
	'category_post':category_post

	}
	return render(request, 'Theblog/categories.html',context)

def LikeView(request, pk):
	post=get_object_or_404(Post, id=request.POST.get('post_id'))
	liked=False
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		liked=False
	else:
		post.likes.add(request.user)
		liked=True
	return HttpResponseRedirect(reverse('article_detail',args=[str(pk)]))


def export_PostData_csvView(request):
	response=HttpResponse(content_type='text/csv')

	writer=csv.writer(response)
	writer.writerow(['Title','Author','Category','Snippet','Body','Published Date','Likes','Views'])

	for data in Post.objects.all().values_list('title','author','category','snippet','body','published_date','likes','blog_views'):
		writer.writerow(data)

	response['Content-Disposition']='attachment; filename="post.csv"'
	return response

def export_PostData_ExcelView(request):
	response=HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition']='attachment; filename="post.xls"'


	wb=xlwt.Workbook(encoding='utf-8')
	ws=wb.add_sheet('Post')
	

	row_num=0
	font_style=xlwt.XFStyle()
	font_style.font.bold=True

	columns=['Title','Author','Category','Snippet','Body','Published Date','Likes','Views']


	for col_num in range(len(columns)):
		ws.write(row_num,col_num,columns[col_num],font_style)

	font_style=xlwt.XFStyle()

	rows=Post.objects.all().values_list('title','author','category','snippet','body','published_date','likes','blog_views')
	for row in rows:
		row_num+=1
		col_num += 1 

		# value = getattr(obj, row.name)

		# if isinstance(value, date):
		# 	value = value.strftime('%d/%m/%Y') 
		# 	data_row.append(value)
		# try:
		# 	ws.write(row_num, col_num, value)

		# except:
		# 	ws.write(row_num, col_num, str(value))

		for col_num in range(len(row)):
			ws.write(row_num,col_num,row[col_num],font_style)

	wb.save(response)


	return response
