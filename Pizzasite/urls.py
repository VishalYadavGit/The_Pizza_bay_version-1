from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from pizza_bay.views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('pizza_bay.urls')),
    path('login',login_page,name='login'),
    path('register',register_page,name='register'),
    path('add-cart/<pizza_uid>',add_cart,name='add_cart'),
    path('register',include('pizza_bay.urls')),
    path('cart',cart,name='cart'),
    path('details',address_ord,name='details'),
    path('logout',signout,name='logout'),
    path('takemail',takemail,name='mail'),
    path('confirmation',confirmation,name='confirmation'),
    path('remove_cart_items/<cart_item_uid>',remove_cart_items,name='remove_cart_items'),
    path('proceed-to-pay',razorpaycheck,name="razorpaycheck"),
    path('order_done',orderdone,name="order-done"),
    path('home',include('pizza_bay.urls')),
    path('about',include('pizza_bay.urls')),
    path('contact',include('pizza_bay.urls')),
    path('order',include('pizza_bay.urls')),
]
# static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
        
urlpatterns += staticfiles_urlpatterns()