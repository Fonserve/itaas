from django.shortcuts import render, redirect
from django.contrib.auth import login
from accounts.forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'frontend/register.html', {'form': form})
    
def landingView(request):
    context = {
        'title': 'Welcome to Our Service',
        'description': 'Explore our features and services to get started.',
        'cta_text': 'Sign Up Now',
    }
    return render(request, 'frontend/landing_page.html', context)