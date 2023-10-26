from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models import Sum


class Basemodel(models.Model):
    uid=models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)

    class Meta:
        abstract=True;

class PizzaCategory(Basemodel):
    category_name=models.CharField(max_length=100)

class Pizza(Basemodel):
    category=models.ForeignKey(PizzaCategory,on_delete=models.CASCADE,related_name="pizzas") 
    pizza_name=models.CharField(max_length=100)
    price=models.IntegerField(default=300)
    image=models.ImageField(upload_to='pizza')

class Cart(Basemodel):
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,related_name="carts")
    is_paid=models.BooleanField(default=False)

    def get_cart_total(self):
        return CartItems.objects.filter(cart=self).aggregate(Sum('pizza__price'))['pizza__price__sum']


class CartItems(Basemodel):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cart_items")
    pizza=models.ForeignKey(Pizza,on_delete=models.CASCADE)

class details(Basemodel):
     user=models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,related_name="details")
     email=models.EmailField(max_length=254)
     address=models.CharField(max_length=200)
     phone=models.IntegerField()
     city=models.CharField(max_length=30)
     state=models.CharField(max_length=30)
     zip=models.IntegerField()
     payment_id=models.CharField(max_length=100,default="Cash on delivery.",null=False,blank=False)
    
class newsletter(models.Model):
    email=models.EmailField(max_length=100)