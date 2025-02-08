from django.shortcuts import render


# Create your views here.
def LandingView(request):
    context = {
        'title': 'Welcome to Our Service',
        'description': 'Explore our features and services to get started.',
        'cta_text': 'Sign Up Now',
    }
    return render(request, 'landing/landing_page.html', context)
