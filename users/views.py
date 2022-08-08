from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import get_user_model


# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, "Your account has been created. You're now allowed login")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES,
                                   instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/profile.html', context)


def Follow(request, email):

    other_user = get_user_model().objects.get(email=email)
    other_user_profile = Profile.objects.get(user=other_user)
    session_user = request.user

    if session_user != other_user:
        if other_user not in session_user.profile.following.all():
            session_user.profile.following.add(other_user)
        else:
            session_user.profile.following.remove(other_user)

        if session_user not in other_user_profile.followers.all():
            other_user_profile.followers.add(session_user)
        else:
            other_user_profile.followers.remove(session_user)

    return HttpResponseRedirect(reverse('user-posts', args=[str(email)]))

