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

def makeOrder(request, product_id):
  if request.method == 'POST':
    product = Product.objects.get(id=id)
    Order.objects.create(
      ''
    )

def payOrder(request, order_id):
  return render(request, 'payorder.html')

@login_required(login_url='login')
def viewDashboard(request):
  orders = Order.objects.filter(client__user=request.user)
  completed = orders.filter(complete=True)[:3]
  orders = orders.order_by('-date')[:3]
  context = {
      'orders': orders,
      'completed':completed,
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
def viewOrder(request, order_id):
  order = Order.objects.get(id=order_id)
  return redirect("/client/payOrder/" + str(order.order_id))

@login_required(login_url='login')
def Logout(request):
	logout(request)
	return redirect('login')

def createpayment(request, order_id):

  order = Order.objects.get(order_id=order_id)
  ppe = "allstartechnologies1@gmail.com"
  domain = "https://canwecleanit.com/client/"

  context = {
      'domain':domain,
      'order': order,
      'ppe': ppe,
  }
  return render(request, 'pay-order.html', context)


def executepayment(request, email, order_id, id):
  order = Order.objects.get(id=id)
  print(order_id)
  domain = "https://canwecleanit.com/client/"
  if request.method == 'POST':
    print("Post detected")
    if order.complete == True:
      print("Order was already complete")
      pass
    else:
      order.complete = True
      order.save()
      print("Order Complete")

      # Send email starting
      server = smtplib.SMTP('smtp.gmail.com', 587)
      server.ehlo()
      server.starttls()
      server.ehlo()
      
      #This can be changed to a HTML file too but I didn't make a template OWO
      link = str(domain) + "/adminViewOrder/" + str(order.order_id)

      main_email = "sanantonioswebdesign@gmail.com"
      server.login("email.canwecleanit@gmail.com", "ylgacvdaekexillh")
      subject = 'An order has been completed'
      title = "Order #" + str(order_id)
      body = f"Hello there! An order is complete and here is what needs! View the link here: {link}"
      
      #Send email to ADMIN
      msg = f"Subject: {subject}\n\n{title}\n{body}"
      server.sendmail(
          'Order #' + str(order_id),
          main_email,
          msg
      )
      print("Sent Email #1")

      #Send email to CLIENT / BUYER
      link = str(domain) + "/payOrder/" + str(order.order_id)
      body = f"Hello there! Looks like you have made a purchase at CanWeCleanIt! View your order here. {link} . If anything we'll send you an email!"
      msg2 = f"Subject: {subject}\n\n{title}\n{body}"
      email = order.email
      server.sendmail(
          'Order #' + str(order_id),
          email,
          msg2
      )
      print("Sent Email #2")

  return HttpResponse("Status 200")

@login_required(login_url='login')
def adminViewOrderProgress(request, order_id):

  order = Order.objects.get(order_id=order_id)
  address_order = order.address.id
  address = Address.objects.get(id=address_order)
  shipped = order.get_shipped_display()

  #Make this only accessable for admins
  if request.user.is_superuser:
    pass
  else:
    return HttpResponse("Hey what are you doing here!")

  if request.method == 'POST':
    instance = request.POST.get("process")
    if str(instance) == "['Not processed', 'Not processed']":
      order.shipped = "Not processed"
    elif str(instance) == "['Out on delivery', 'Out on delivery']":
      order.shipped = "Out on delivery"
      server = smtplib.SMTP('smtp.gmail.com', 587)
      server.ehlo()
      server.starttls()
      server.ehlo()

      main_email = order.email
      link = "https://canwecleanit.com/client/payOrder/" + str(order.order_id)
      server.login("email.canwecleanit@gmail.com", "ylgacvdaekexillh")
      subject = 'An order has been marked "Out on delivery."'
      title = "Order #" + str(order.order_id)
      body = f'Hello, your order has been marked "Out on delivery" for more information: {link}'
    else:
      pass
    
    order.save()

  context = {
    'order':order,
    'shipped':shipped,
    'address':address
  }

  return render(request, 'adminViewOrder.html', context)
