from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from accounts.forms import CustomUserCreationForm

def register(request):
    if request.user.is_authenticated:
        return redirect('frontend:myaccount')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('frontend:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'frontend/register.html', {'form': form})

def loginView(request):
    if request.user.is_authenticated:
        return redirect('frontend:home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('frontend:home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'frontend/login.html', {'form': form})
    
def landingView(request):
    cta_text = 'Sign Up Now'
    if request.user.is_authenticated:
        cta_text = 'My Dashboard'
    context = {
        'title': 'Welcome to Our Service',
        'description': 'Explore our features and services to get started.',
        'cta_text': cta_text,
    }
    return render(request, 'frontend/landing_page.html', context)

@login_required
def myAccount(request):
    return render(request, 'frontend/my_account.html')

def logoutView(request):
    logout(request)
    return redirect('frontend:home')