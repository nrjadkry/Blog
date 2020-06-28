
from django.urls import path
from .views import UserRegisterView, UserEditView, PasswordsChangeView, password_success,profile
from django.contrib.auth import views as auth_views
from . import views

from django.contrib.auth.decorators import login_required

urlpatterns = [
	path('register/',UserRegisterView.as_view(),name='register'),
	path('edit_profile/',login_required(UserEditView.as_view(),login_url='login'),name='edit_profile'),
	# path('password/',auth_views.PasswordChangeView.as_view(template_name='registration/change_password.html')),
	path('password/',login_required(PasswordsChangeView.as_view(),login_url='login')),
	path('password_success/',login_required(views.password_success,login_url='login'),name='password_success'),
	path('profile/',views.profile,name='profile'),

	

]