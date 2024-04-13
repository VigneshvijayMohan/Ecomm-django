from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms


# Create your views here.


def home(request):
    products = Product.objects.all()
    categories = set(product.category for product in products)
    return render(request, "store/home.html", {"products":products, "categories":categories})


def about(request):
    return render(request, "store/about.html", {})


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been Logged in.."))
            return redirect('home')
        else:
            messages.success(request, ("There was an error, please try again."))
            return redirect('login')
    else: 
        return render(request, "store/login.html", {})


def logout_user(request):
	logout(request)
	messages.success(request, ("You have been logged out...Thanks for stopping by..."))
	return redirect('home')


def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# log in user
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Username Created - Please Fill Out Your User Info Below..."))
			return redirect('update_info')
		else:
			messages.success(request, ("Whoops! There was a problem Registering, please try again..."))
			return redirect('register')
	else:
		return render(request, 'store/register.html', {'form':form})



def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, "store/product.html", {"product":product})

def category(request, foo):
    foo = foo.replace("-", " ")
    products = Product.objects.filter(category__name=foo)
    all_products = Product.objects.all()
    categories = set(product.category for product in all_products)
    return render(request, "store/home.html", {"products":products, "categories":categories})


