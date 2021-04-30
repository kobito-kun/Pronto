from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from clean.views import *
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # Administration
    path('admin/', admin.site.urls),

    # Client
    path('', viewMain, name="main"),
    path('login/', Login, name="login"),
    path('signup/', Signup, name="signup"),
    path('logout/', Logout, name='logout'),
    path('products/', viewProducts, name="products"),
    path('payOrder/<str:order_id>', csrf_exempt(payOrder)),
    path('createOrder/qty=<int:qty>/id=<int:id>', createOrder),

    path('adminViewOrder/<str:order_id>', adminViewOrderProgress),

    path('dashboard/', viewDashboard, name="dashboard"),
    path('dashboard/orders', viewOrders, name="orders"),
    path('dashboard/viewOrder/<int:order_id>', viewOrder),

    path('my-api/execute-payment/elsemail=<str:email>&order_id=<str:order_id>&id=<str:id>',
         csrf_exempt(executepayment), name='executepayment'),
    path('my-api/create-payment/<str:order_id>',
         csrf_exempt(createpayment), name='createPayment'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)