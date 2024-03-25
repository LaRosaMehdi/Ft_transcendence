from django.contrib import messages
from django.contrib.auth import login
from smtp.views.forms import TwoFactorForm
from django.shortcuts import render, redirect

from users.views import *
from users.models import User
from smtp.views.forms import TwoFactorForm

def twofactor_oauth(request):
    if request.method == 'POST':
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            validation_code = form.cleaned_data['validation_code']
            user_id = request.session.get('user_id')
            if user_id:
                user = User.objects.get(id=user_id)
                if user.validation_code == validation_code:
                    # Clear validation code after successful validation
                    user.validation_code = None
                    user.save()
                    user_set_is_connected(user)
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, "Invalid validation code", extra_tags='twofactor_oauth_tag')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}", extra_tags='twofactor_oauth_tag')
    else:
        messages.error(request, "Invalid request method", extra_tags='twofactor_oauth_tag')
    return redirect('twofactor')