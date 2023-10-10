from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages

from item.models import Category, Item

from .forms import SignupForm
# Create your views here.

def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()

    return render(request, 'core/index.html' , {
        'categories': categories,
        'items': items,
    })

def contact(request):
    return render(request, 'core/contact.html')

# Using Django built in forms
def signup(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)
        # Check if form inputs are valid
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
    # Create form
        form = SignupForm()

    return render(request, 'core/signup.html', {
        # Add to render
        'form': form
    })

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('core:index')