from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(PizzaCategory)
admin.site.register(Pizza)
admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(details)
admin.site.register(newsletter)
