from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.urls import reverse_lazy
from .forms import SignUpForm, EditProfileForm, PasswordChangingForm, ProfilePicUpdateForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib.auth.models import User


# Create your views here.
class UserRegisterView(generic.CreateView):
	form_class=SignUpForm
	template_name='registration/registration.html'
	success_url=reverse_lazy('login')

# @login_required(login_url='login')
class UserEditView(generic.UpdateView):

	form_class=EditProfileForm
	template_name='registration/edit_profile.html'
	success_url=reverse_lazy('home')


	def get_object(self):
		return self.request.user


class PasswordsChangeView(PasswordChangeView):
	# form_class=PasswordChangeForm

	form_class=PasswordChangingForm
	template_name='registration/change_password.html'
	success_url=reverse_lazy('password_success')




def password_success(request):
	context={}
	return render(request, 'registration/password_success.html',context)




@login_required(login_url='login')
def profile(request):
	return render(request,'registration/user_profile.html')


class EditProfilePageView(generic.UpdateView):
	model=UserProfile
	template_name='registration/edit_profile_page.html'
	fields=['bio','profile_picture']
	success_url=reverse_lazy('home')
