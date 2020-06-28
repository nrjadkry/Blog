
from django.urls import path, include
from . import views
from .views import HomeView, ArticleDetailView, CreateBlogView, UpdatePostView, DeletePostView, CreateCategoryView, CategoryView, CategoryListView, LikeView, UserArticleView, export_PostData_csvView, export_PostData_ExcelView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('article/<str:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('createblog/', CreateBlogView.as_view(), name='createblog'),
    path('createcategory/', CreateCategoryView.as_view(), name='createcategory'),
    path('article/edit/<str:pk>/', UpdatePostView.as_view(), name='upateblog'),
    path('article/delete/<str:pk>/', DeletePostView.as_view(), name='deleteblog'),
    path('category/<str:cate>/', CategoryView, name='category'),
    path('categories/',CategoryListView.as_view(),name='categories'),
    path('like_post/<str:pk>/',LikeView,name='like_post'),
    path('myarticles/<str:username>/',UserArticleView,name='user_article'),
    path('export_PostData_csv/',views.export_PostData_csvView,name='export-csv'),
    path('export_PostData_xls/',views.export_PostData_ExcelView,name='export-xls'),
    path('import_category/',views.import_category,name='import_category'),




    # path('hitcount/',include('hitcount.urls','hitcount'),namespace='hitcount'),


]