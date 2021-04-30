# Django Imports
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect

# Personal Imports
from .forms import *
from .decorator import *
from .models import *
import uuid
import smtplib

@unauthenticated_user
def Login(request):
  message = ""
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      return redirect('dashboard')
    else:
      message = 'Username Or Password Incorrect.'
  context = {
      'message': message,
  }
  return render(request, 'login.html', context)

@unauthenticated_user
def Signup(request):
  form = CreateUserForm()
  if request.method == 'POST':
    form = CreateUserForm(request.POST)
    if form.is_valid():
      user = form.save()
      username = form.cleaned_data.get('username')
      email = form.cleaned_data.get('email')
      Client.objects.create(user=user, email=email)
      print("A user has signed up.")
      return redirect('login')
  context = {
      'form': form,
  }
  return render(request, 'register.html', context)

def viewMain(request):
  return render(request, 'index.html')

def viewProducts(request):
  products = Product.objects.all()

  context = {
      'products': products
  }
  return render(request, 'products.html', context)

def createOrder(request, qty, id):
  product = Product.objects.get(id=id)
  total = float(qty) * float(product.price)
  order = Order.objects.create(
    order_id = uuid.uuid4(),
    product = product,
    total = total,
  )
  if request.user.is_authenticated:
    client = Client.objects.get(user__username=request.user)
    order.name = str(client.user)
    order.email = str(client.email)
    order.client = client
    order.save()
  return redirect(f'/payOrder/{order.order_id}')

def payOrder(request, order_id):
  order = Order.objects.get(order_id=order_id)
  quantity = int(float(order.total) / float(order.product.price))
  
  if request.method == 'POST':
    user = request.POST.get("username")
    email = request.POST.get("email")
    order.name = user
    order.email = email
    order.save()
    return redirect(f'/payOrder/{order.order_id}')

  context = {
    'order':order,
    'quantity': quantity
  }
  return render(request, 'payorder.html', context)

@login_required(login_url='login')
def viewDashboard(request):
  orders = Order.objects.filter(client__user=request.user)
  completed = orders.filter(complete=True)
  latest = orders.order_by('-date')[:3]

  total = 0
  for p in completed:
    total += float(p.total)

  context = {
      'orders': orders,
      'completed':completed,
      'total': total,
      'latest': latest
  }
  return render(request, 'dashboard/main.html', context)

@login_required(login_url='login')
def viewOrders(request):
  order = Order.objects.filter(client__user=request.user)
  completed = order.filter(complete=True)
  context = {
      'completed':completed,
      'order': order
  }
  return render(request, 'dashboard/orders.html', context)

@login_required(login_url='login')
def Logout(request):
	logout(request)
	return redirect('login')

def createpayment(request, order_id):
  order = Order.objects.get(order_id=order_id)
  ppe = "null@nukll.com"
  domain = request.META["HTTP_HOST"] # request.get_host()
  domain = f"https://{domain}"

  context = {
      'domain':domain,
      'order': order,
      'ppe': ppe,
  }
  return HttpResponse("Payments currently disabled")
  #return render(request, 'pay-order.html', context)


def executepayment(request, email, order_id, id):
  order = Order.objects.get(id=id)
  print(order_id)
  domain = f"https://{request.get_host()}"
  if request.method == 'POST':
    print("Post detected")
    if order.complete == True:
      print("Order was already complete")
      pass
    else:
      order.complete = True
      order.save()
  return HttpResponse("Status 200")
