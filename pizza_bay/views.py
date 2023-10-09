from django.shortcuts import render,redirect
# from locust import User
from pizza_bay.models import *
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout

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

def add_cart(request,pizza_uid):
    user=request.user
    pizza_obj=Pizza.objects.get(uid=pizza_uid)
    cart , _ =Cart.objects.get_or_create(user=user, is_paid=False)

    cart_items=CartItems.objects.create(
        cart=cart,
        pizza=pizza_obj
    )
    return redirect('/')

def cart(request):
    cart=Cart.objects.get(is_paid=False,user=request.user)
    context={'carts':cart}
    return render(request,'cart.html',context)

def remove_cart_items(request,cart_item_uid):
    try:
        CartItems.objects.get(uid=cart_item_uid).delete()

        return redirect('cart')
    except Exception as e:
        print(e)

def address_ord(request):
    if(request.method=='POST'):
        try:
            user=request.user
            Address=request.POST.get('address')
            Email=request.POST.get('email')
            Phone=request.POST.get('phone')
            City=request.POST.get('city')
            State=request.POST.get('state')
            Zip=request.POST.get('zip')
            # Address=request.POST.get('address')
            details.objects.create(
                user=user,
                address=Address,
                email=Email,
                phone=Phone,
                city=City,
                state=State,
                zip=Zip)
            return redirect('confirmation')
        except Exception as e:
            print('e')
            return redirect('details')
        

    return render(request,'details.html')

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