from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Follow
from .forms import ProfileForm
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/registration.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Logged in successfully.'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials.'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@login_required
def user_logout(request):
    logout(request)
    return JsonResponse({'message': 'Logged out successfully.'}, status=200)

@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    following = Follow.objects.filter(follower=request.user, following=user).exists()
    return render(request, 'users/profile.html', {'profile': profile, 'following': following})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm

@login_required
def edit_profile(request, username):

    profile = get_object_or_404(Profile, user__username=username)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'users/profile_edit.html', {'form': form})

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if user_to_follow != request.user:
        Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('profile', username=username)

@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('profile', username=username)
