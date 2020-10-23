from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=True)
    phone=models.CharField(max_length=200,null=True)
    email=models.EmailField(max_length=250,null=True)
    date_created=models.DateTimeField(auto_now_add=True)
    profile_pic=models.ImageField(default="profile1.png",null=True,blank=True)

    def __str__(self):
        return str(self.name)

class Tag(models.Model):
    name=models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY=(
                ('indoor','indoor'),
                ('outdoor','outdoor'),
            )
    name=models.CharField(max_length=200,null=True)
    price=models.DecimalField(max_digits = 5, decimal_places = 2) 
    category=models.CharField(max_length=200,null=True,choices=CATEGORY)
    description=models.CharField(max_length=200,null=True,blank=True)
    date_created=models.DateTimeField(auto_now_add=True)
    tags=models.ManyToManyField(Tag)
    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS=(
                ('Delivered','Delivered'),
                ('Pending','Pending'),
                ('Out for delivery','Out for delivery'),
            )
    customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    status=models.CharField(max_length=200,null=True,choices=STATUS)
    date_created=models.DateTimeField(auto_now_add=True)
    note=models.CharField(max_length=1000,null=True)
    def __str__(self):
        return str(self.id)


