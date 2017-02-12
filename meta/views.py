from avatar.forms import UploadAvatarForm
from datetime import datetime
from django.utils import timezone
from avatar.models import Avatar
from avatar.signals import avatar_updated
from datetime import date
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Q, Sum
from django.db import connection, transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.db.models import Max
from fbf import settings
from itertools import groupby
from mailchimp3 import MailChimp
from meta.forms import ChangeEmailForm, RegistrationForm, ProfileForm, DocumentForm, ProfileFormAddress
from meta.models import Profile
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import math
import re
import time
from django.utils import timezone
from django.core import serializers
import json
import datetime
import os

def index(request):

    return render(request, 'meta/index.html')

def about(request):
    return render(request, 'meta/about.html')


@transaction.atomic
def register(request):
    next_url = request.POST.get('next', request.GET.get('next', reverse('profile')))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        profileform = ProfileForm(request.POST)
        if form.is_valid() and profileform.is_valid():
            new_user = form.save()
            profile = profileform.save(commit=False)
            if profile.user_id is None:
                profile.user_id = new_user.id
            profile.save()
    
            # Login the newly created user.
            authenticated_user = authenticate(username=new_user.username,
                                              password=form.cleaned_data['password1'])
            login(request, authenticated_user)
            return redirect(next_url)
    else:
        form = RegistrationForm()
        profileform = ProfileForm()
    return render(request, 'meta/register.html', {'form': form, 'profileform': profileform, 'next': next_url})


@login_required
def profile(request, extra_context={}):
    path="media/" + request.user.username + "/" # insert the path to your directory
    
    if (os.path.isdir(path)):
        num_files = len([f for f in os.listdir(path)
                     if os.path.isfile(os.path.join(path, f))])
        img_list =os.listdir(path)
    
    else:
    
        num_files = 0
        img_list = ""
    
    username = request.user.username
    
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('profile')
    else:
        form = DocumentForm()
        form_address = ProfileFormAddress()
    return render(request, 'meta/profile.html', {
                  'form': form,
                  'images': img_list,
                  'username': username,
                  'num_files': num_files,
                  'form_address': form_address,
                  })


@login_required
def change_email(request):
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            request.user.email = form.cleaned_data['new_email']
            request.user.save()
            messages.success(request, 'Your e-mail address has been changed.')
            return redirect(reverse('profile'))
    else:
        form = ChangeEmailForm()
    return render(request, 'meta/changeemail.html', {'form': form})


@require_POST
@login_required
def change_avatar(request):
    '''Customised version of the default add avatar view from the django-avatar
    app. Changed to allow the form to be embedded on the main DWAD profile
    page.'''
    upload_avatar_form = UploadAvatarForm(request.POST or None,
                                          request.FILES or None,
                                          user=request.user)
    if 'avatar' in request.FILES and upload_avatar_form.is_valid():
        avatar = Avatar(user=request.user, primary=True)
        image_file = request.FILES['avatar']
        avatar.avatar.save(image_file.name, image_file)
        avatar.save()
        avatar_updated.send(sender=Avatar, user=request.user, avatar=avatar)
        return redirect(reverse('profile'))
    context = {'upload_avatar_form': upload_avatar_form}
    return profile(request, extra_context=context)


@login_required
def password_changed(request):
    messages.success(request, 'Your password has been changed.')
    return redirect(reverse('profile'))


def password_reset_requested(request):
    messages.success(request,
                     '''A password reset link has been sent to the e-mail
                     address you provided. Please follow the link to set your
                     new password.''')
    return redirect(reverse('login'))
