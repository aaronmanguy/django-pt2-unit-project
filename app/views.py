from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from .decorators import *
from .models import *
from .forms import *

# Create your views here.
def home(request):
    products = Product.objects.all().order_by('-date_created')
    context = {'products':products}
    return render(request, 'home.html', context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['user', 'admin'])
def createProduct(request):
    form = CreateProduct()
    if request.method == "POST":
        form = CreateProduct(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
        
    context = {'product':form}
    return render(request, 'create-product.html', context)


def viewProduct(request, pk):
    product = Product.objects.get(id=pk)
    context = {'product':product}
    return render(request, "view-product.html", context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
# def all_users(request):
#     users = User.objects.all().order_by('-date_joined')
#     context = {'users': users}
#     return render(request, 'admin.html', context)

@unauthenticated_user
def registerPage(request):
        form = CreateUser()

        if request.method == 'POST':
            form = CreateUser(request.POST)
            if form.is_valid():
                user = form.save()
                messages.success(request, 'Account successfully created. Please log in.')

                group = Group.objects.get(name='user')
                user.groups.add(group)
                Seller.objects.create(user=user, name=user)

                return redirect('/login')

        context = {'form':form}
        return render(request, 'register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username or Password is incorrect')
    return render(request, 'login.html')

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('/login')

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['user', 'admin'])
def profilePage(request, pk):
    seller = Seller.objects.get(id=pk)
    products = Product.objects.filter(seller=seller).order_by('-date_created')
    context = {'products':products, 'seller':seller}
    return render(request, 'profile.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['user', 'admin'])
def editProfile(request):
    form = SellerProfile(instance=request.user.seller)

    if request.method == 'POST':
        form = SellerProfile(request.POST, request.FILES, instance=request.user.seller)
        if form.is_valid():
            form.save()
            return redirect('/profile')
        
    context = {'form': form}
    return render(request, 'edit-profile.html', context)



# @login_required(login_url='login')
# @allowed_users(allowed_roles=['user', 'admin'])
# def deletePost(request, pk):
#     post = Post.objects.get(id=pk)
#     if request.method == "POST":
#         post.delete()
#         return redirect('/profile')
#     context = {'post': post}
#     return render(request, 'delete-post.html', context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
# def delete_user(request, pk):
#     user = User.objects.get(id=pk)
#     if request.method == "POST":
#         user.delete()
#         return redirect('/all-users')
#     context = {'user': user}
#     return render(request, 'delete-user.html', context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['user', 'admin'])
# def self_user_delete(request, pk):
#     user = User.objects.get(id=pk)
#     if request.method == "POST":
#         user.delete()
#         return redirect('/login')
#     context = {'user': user}
#     return render(request, 'user-delete-user.html', context)