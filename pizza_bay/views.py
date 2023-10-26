from django.shortcuts import render,redirect
# from locust import User
from pizza_bay.models import *
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    pizzas=Pizza.objects.all()
    context = {"pizzas":pizzas}
    return render(request,'index.html',context)
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')
def order(request):
    return render(request,'order.html')


def login_page(request):
    if (request.method=='POST'):
        try:
            username=request.POST.get('username')
            password=request.POST.get('password')

            user_obj=User.objects.filter(username=username)
            if not user_obj.exists():
                messages.error(request, "User not Found.")
                return redirect('login')
            
            user_obj=authenticate(username=username,password=password)
            if user_obj:
                login(request,user_obj)
                return redirect('/')
            
            messages.error(request,"Incorrect Password.")

        except Exception as e:
            messages.error(request,"Something Went Wrong!")


    return render(request,'login.html')




def register_page(request):
    if (request.method=='POST'):
        
        try:
            username=request.POST.get('username')
            password=request.POST.get('password')

            user_obj=User.objects.filter(username=username)
            if user_obj.exists():
                messages.error(request, "Username is taken.")
                return redirect('register')
            
            user_obj=User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request, "Account created Succesfully. Login Now!")
            return redirect("login")

        except Exception as e:
            messages.error(request,"Something Went Wrong!")

    return render(request,'register.html')

@login_required(login_url='login')
def add_cart(request,pizza_uid):
    if request.user.is_authenticated:
        user=request.user
        pizza_obj=Pizza.objects.get(uid=pizza_uid)
        cart , _ =Cart.objects.get_or_create(user=user, is_paid=False)

        cart_items=CartItems.objects.create(
            cart=cart,
            pizza=pizza_obj
        )
        return redirect('/')
    return redirect('login')

@login_required(login_url='login')
def cart(request):
    cart=Cart.objects.get_or_create(is_paid=False,user=request.user)
    context={'carts':cart}
    return render(request,'cart.html',context)

def remove_cart_items(request,cart_item_uid):
    try:
        CartItems.objects.get(uid=cart_item_uid).delete()

        return redirect('cart')
    except Exception as e:
        print(e)

@login_required(login_url='login')
def address_ord(request):
    carttest=Cart.objects.get(is_paid=False,user=request.user)
    
    if(request.method=='POST'):
        try:
            user=request.user
            Address=request.POST.get('address')
            Email=request.POST.get('email')
            Phone=request.POST.get('phone')
            City=request.POST.get('city')
            State=request.POST.get('state')
            Zip=request.POST.get('zip')
            payment_id=request.POST.get('order_id')
            # Address=request.POST.get('address')
            details.objects.create(
                user=user,
                address=Address,
                email=Email,
                phone=Phone,
                city=City,
                state=State,
                zip=Zip,
                payment_id=payment_id)
            cart=Cart.objects.get(user=request.user)
            cart.is_paid=True
            cart.save()
            return redirect('confirmation')
        except Exception as e:
            print('e')
            return redirect('details')
        
    elif(Cart.get_cart_total(carttest)==None):
         return redirect('/')
    return render(request,'details.html')

@login_required(login_url='login')
def confirmation(request):
    return render(request,'confirmation.html')


def signout(request):
    logout(request)
    return redirect('/')


def takemail(request):
    if(request.method=='POST'):
        mail=request.POST.get('mail')
        newsletter.objects.create(
            email=mail
        )
        return redirect('/')
    
    return render(request,'contact.html')


def razorpaycheck(request):
    cart=Cart.objects.get(is_paid=False,user=request.user)
    total_price=Cart.get_cart_total(cart)
    print(total_price)
    return JsonResponse({
        'total_price':total_price
    })

def orderdone(request):
    pass
