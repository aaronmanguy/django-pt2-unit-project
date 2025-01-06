from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from .decorators import *
from .models import *
from .forms import *
from django.views import View
from django.http import JsonResponse
from django.conf import settings
import stripe


stripe.api_key = "sk_test_51QdD5bGGQnr91qVirbcauJSweVve4v1vAwWJ4Ts9sQ6izGBM51F4NzFT819sqZwnGMB9gna4cfHJHYbUR3FPa7Aq00BHOWTCzx"

from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def home(request):
    products = Product.objects.all().order_by("-date_created")
    context = {"products": products}
    return render(request, "home.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["user", "admin"])
def createProduct(
    request,
):  # a comment as a book mark for the create product def so we dont pass it
    form = CreateProduct()
    if request.method == "POST":
        form = CreateProduct(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            product = stripe.Product.create(name=form.cleaned_data["name"])
            price = stripe.Price.create(
                product=product.id,
                unit_amount=form.cleaned_data["price"],
                currency="usd",
            )
            products = Product.objects.all().order_by("-date_created")
            context = {"price":price, "products":products}
            return render(request, "home.html", context)

    context = {"product": form}

    return render(request, "create-product.html", context)



def viewProduct(request, pk):
    product = Product.objects.get(id=pk)
    p = stripe.Price.list().data[0]

    # prod = stripe.products.retrieve(product.id)

    payment_link = stripe.PaymentLink.create(
        line_items=[
            {
                "price": p.id,
                "quantity": 1,
            },
        ],
        automatic_tax={"enabled": True},
    )
    context = {"product": product, "p": p, "payment_link": payment_link}
    return render(request, "view-product.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def all_users(request):
    users = User.objects.all().order_by('-date_joined')
    context = {'users': users}
    return render(request, 'all-users.html', context)


@unauthenticated_user
def registerPage(request):
    form = CreateUser()

    if request.method == "POST":
        form = CreateUser(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account successfully created. Please log in.")

            group = Group.objects.get(name="user")
            user.groups.add(group)
            Seller.objects.create(user=user, name=user)

            return redirect("/login")

    context = {"form": form}
    return render(request, "register.html", context)


@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Username or Password is incorrect")
    return render(request, "login.html")


@login_required(login_url="login")
def logoutUser(request):
    logout(request)
    return redirect("/login")


def profilePage(request, pk):
    try:
        seller = Seller.objects.get(id=pk)
    except ObjectDoesNotExist:
        seller_exists = False
    else:
        seller_exists = True

    if seller_exists == False:
        return render(request, 'no-seller.html')

    products = Product.objects.filter(seller=seller).order_by('-date_created')
    context = {'products':products, 'seller':seller}
    return render(request, 'profile.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["user", "admin"])
def editProfile(request, pk):
    form = SellerProfile(instance=request.user.seller)

    if request.method == "POST":
        form = SellerProfile(request.POST, request.FILES, instance=request.user.seller)
        if form.is_valid():
            form.save()
            return redirect("/profile/" + str(pk))

    context = {"form": form}
    return render(request, "edit-profile.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["user", "admin"])
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == "POST":
        product.delete()
        return redirect("/")
    context = {"product": product}
    return render(request, "delete-product.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_user(request, pk):
    user = User.objects.get(id=pk)
    if request.method == "POST":
        user.delete()
        return redirect('/all-users')
    context = {'user': user}
    return render(request, 'delete-user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['user', 'admin'])
def self_user_delete(request, pk):
    user = User.objects.get(id=pk)
    if request.method == "POST":
        user.delete()
        return redirect('/login')
    context = {'user': user}
    return render(request, 'user-delete-user.html', context)
