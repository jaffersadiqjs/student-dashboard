from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from .models import StudentProfile

def user_login(request):
    next_url = request.GET.get('next', '/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard_view(request):
    # Automatically create StudentProfile if not exists
    student, created = StudentProfile.objects.get_or_create(
        user=request.user,
        defaults={'attendance': 0, 'grade': 'N/A'}
    )
    return render(request, 'dashboard.html', {'student': student})

def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')
