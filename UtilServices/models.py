from email.policy import default
from random import choices
from django.contrib.auth.models import User
from django.db import models


STATE_CHOICES=(
    ('Andhra Pradesh' , 'Andhra Pradesh'),
    ('Arunachal Pradesh' , 'Arunachal Pradesh'),	
    ('Assam' , 'Assam'),	
    ('Bihar' , 'Bihar'),	
    ('Chhattisgarh' , 'Chhattisgarh'),	
    ('Goa' , 'Goa'),	
    ('Gujarat' , 'Gujarat'),	
    ('Haryana' , 'Haryana'),	
    ('Himachal Pradesh' , 'Himachal Pradesh'),	
    ('Jharkhand' , 'Jharkhand'),
    ('Karnataka' , 'Karnataka'),	
    ('Kerala' , 'Kerala'),	
    ('Madhya Pradesh' , 'Madhya Pradesh'),	
    ('Maharashtra' , 'Maharashtra'),	
    ('Manipur' , 'Manipur'),	
    ('Meghalaya' , 'Meghalaya'),	
    ('Mizoram' , 'Mizoram'),	
    ('Nagaland' , 'Nagaland'),
    ('Odisha' , 'Odisha'),	
    ('Punjab' , 'Punjab'),	
    ('Rajasthan' , 'Rajasthan'),	
    ('Sikkim' , 'Sikkim'),	
    ('Tamil Nadu' , 'Tamil Nadu'),	
    ('Telangana' , 'Telangana'),	
    ('Tripura' , 'Tripura'),	
    ('Uttar Pradesh' , 'Uttar Pradesh'),	
    ('Uttarakhand'	 , 'Uttarakhand'),
)

class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    locality=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(choices=STATE_CHOICES,max_length=50)
    zipcode=models.IntegerField()

    def __str__(self):
        return str(self.id)

CATEGORY_CHOICES=(
    ('L','Laptop'),
    ('M','Mobile'),
    ('TW','Top Wear'),
    ('BW','Bottom Wear'),
    ('S','Shoes'),
)

class Product(models.Model):
    name=models.CharField(max_length=200)
    selling_price=models.FloatField()
    discount_price=models.FloatField()
    description=models.TextField()
    brand=models.CharField(max_length=200)
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image=models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price

STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    order_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(choices=STATUS_CHOICES,default='Pending',max_length=50)

    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price