from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Sellers(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    phone=models.CharField(max_length=10)
    license_no=models.CharField(max_length=100)
    logo=models.CharField(max_length=100,default="")
    place=models.CharField(max_length=100)
    pincode=models.CharField(max_length=10)
    district=models.CharField(max_length=100)
    state=models.CharField(max_length=50)
    latitude=models.CharField(max_length=100)
    longtitude=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    AUTHUSER=models.OneToOneField(User,on_delete=models.CASCADE)


class Customers(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=10)
    gender=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    pincode=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    AUTHUSER=models.OneToOneField(User,on_delete=models.CASCADE)


class Categories(models.Model):
    name=models.CharField(max_length=100)

class Product(models.Model):
    name=models.CharField(max_length=100)
    photo=models.CharField(max_length=400,default="")
    discription=models.CharField(max_length=500)
    price=models.CharField(max_length=100)
    SELLERS=models.ForeignKey(Sellers,on_delete=models.CASCADE)
    CATEGORIES=models.ForeignKey(Categories,on_delete=models.CASCADE)

class Stock(models.Model):
    PRODUCT=models.ForeignKey(Product,on_delete=models.CASCADE)
    stock=models.IntegerField()

class Favourite(models.Model):
    AUTHUSER=models.ForeignKey(User,on_delete=models.CASCADE)
    PRODUCT = models.ForeignKey(Product, on_delete=models.CASCADE)

class Offers(models.Model):
    PRODUCT = models.ForeignKey(Product, on_delete=models.CASCADE)
    offers_price=models.CharField(max_length=100)
    expiry_date=models.DateField()

class Complaints(models.Model):
    date=models.DateField()
    compliant=models.CharField(max_length=500)
    replay=models.CharField(max_length=500)
    status=models.CharField(max_length=500)
    AUTHUSER=models.ForeignKey(User,on_delete=models.CASCADE)

class Review(models.Model):
    date=models.DateField()
    review=models.CharField(max_length=100)
    AUTHUSER=models.ForeignKey(User,on_delete=models.CASCADE)











