from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404
from django.views.generic.list_detail import object_detail
from django.template import RequestContext
from models import Profile
from forms import UserForm

def view_profile(request, username):
	if username is None:	
		if request.user.is_authenticated():		
			username = request.user.username

	user = get_object_or_404(User, username=username)

	return render_to_response(
		'view-profile.html',
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
			return HttpResponseRedirect(profile.get_absolute_url())
	else:
		this_user_form = UserForm(instance=user)

	return render_to_response(
		'edit-profile.html',
		{
			'this_user': user,
			'this_user_form': this_user_form,
		},
		context_instance=RequestContext(request)
	)
