# -*- mode: python; coding: utf-8; -*-
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.http import HttpResponseNotAllowed, HttpResponseForbidden
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from users.models import Profile
from users.forms import UserForm, LoginForm

def view_profile(request, username):
	if username is None:	
		if request.user.is_authenticated():		
			username = request.user.username

	user = get_object_or_404(User, username=username)

	return render_to_response(
		'users/view-profile.html',
		{
			'this_user': user,
			'this_profile': user.get_profile(),
		},
		context_instance=RequestContext(request)
	)

@login_required
def edit_profile(request, username):
	user = get_object_or_404(User, username=username)
	profile = user.get_profile()

	if request.user.pk != user.pk and request.user.has_perm('user.can_change') == False:
		return HttpResponseNotAllowed('You cannot edit this profile.')

	if request.method == 'POST':
		this_user_form = UserForm(request.POST, instance=user)
		if this_user_form.is_valid():
			this_user_form.save()
			return redirect(profile)
	else:
		this_user_form = UserForm(instance=user)

	return render_to_response(
		'users/edit-profile.html',
		{
			'this_user': user,
			'this_user_form': this_user_form,
		},
		context_instance=RequestContext(request)
	)

def login(request):
    from django.contrib.auth import authenticate, login
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(settings.LOGIN_REDIRECT_URL)
                else:
                    return HttpResponseForbidden('Your account is disabled')
            else:
                return HttpResponseForbidden('User does not exist')
    else:
        form = LoginForm()
    
    return render_to_response(
        'users/login.html',
        { 'form': form },
        context_instance=RequestContext(request)
    )
