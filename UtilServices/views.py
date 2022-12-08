import re
from unicodedata import category
from django.shortcuts import render,redirect
from django.views import View
from .forms import CustomerRegistrationForm,CustomerProfileForm
from UtilServices.models import *
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ProductView(View):
    def get(self,request):
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')
        return render(request,'app/home.html',
        {'topwears':topwears,
        'bottomwears':bottomwears,
         'mobiles':mobiles})



# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        item_added=False
        if request.user.is_authenticated:
            item_added=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request,'app/productdetail.html',{'product':product,'item_added':item_added})


@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)

        amount=0.0
        shipping_amount=120.0
        total_amount=0.0

        cart_product = [p for p in Cart.objects.all() if p.user==user]

        if cart_product:
            for p in cart_product:
                temp_amount=(p.quantity *p.product.discount_price)
                amount+=temp_amount
        if amount==0:
            total_amount=0
            shipping_amount=0
        else:
            total_amount=amount+shipping_amount


        return render(request, 'app/addtocart.html',{'carts':cart,'amount':amount,
        'shipping_amount':shipping_amount,'total_amount':total_amount})
    
def cal_billing_amount(request):
    amount=0.0
    shipping_amount=120.0
    total_amount=0.0

    cart_product = [p for p in Cart.objects.all() if p.user==request.user]

    if cart_product:
        for p in cart_product:
            temp_amount=(p.quantity *p.product.discount_price)
            amount+=temp_amount
    total_amount=amount+shipping_amount
    return [amount,shipping_amount,total_amount]


def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.quantity+=1
        c.save()
        amount,shipping_amount,total_amount=cal_billing_amount(request)

        data={
            'quantity':c.quantity,
            'amount':amount,
            'shipping_amount':shipping_amount,
            'total_amount':total_amount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.quantity-=1
        if(c.quantity==0): c.delete()
        else: c.save()
        amount,shipping_amount,total_amount=cal_billing_amount(request)

        data={
            'quantity':c.quantity,
            'amount':amount,
            'shipping_amount':shipping_amount,
            'total_amount':total_amount
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.delete()
        amount,shipping_amount,total_amount=cal_billing_amount(request)

        data={
            'amount':amount,
            'shipping_amount':shipping_amount,
            'total_amount':total_amount
        }
        return JsonResponse(data)

def buy_now(request):
 return render(request, 'app/buynow.html')




@login_required
def orders(request):
    op=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'orderplaced':op})



def mobile(request,data=None):
    if data==None:
        mobiles=Product.objects.filter(category='M')
    else:
        mobiles=Product.objects.filter(category='M').filter(brand=data)

    return render(request, 'app/mobile.html',{'mobiles':mobiles})


def bottomwear(request,data=None):
    if data==None:
        bws=Product.objects.filter(category='BW')
    else:
        bws=Product.objects.filter(category='BW').filter(brand=data)

    return render(request, 'app/bottomwear.html',{'bws':bws})


def topwear(request,data=None):
    if data==None:
        tws=Product.objects.filter(category='TW')
    else:
        tws=Product.objects.filter(category='TW').filter(brand=data)

    return render(request, 'app/topwear.html',{'tws':tws})

def laptop(request):
    
    laptops=Product.objects.filter(category='L')

    return render(request, 'app/laptop.html',{'laptops':laptops})

    




class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})

    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! you have registered successfully.')
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})


@login_required
def checkout(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    amount,shipping_amount,total_amount=cal_billing_amount(request)
    return render(request, 'app/checkout.html',{'addrs':add,
    'total_amount':total_amount,'cart_items':cart_items})

@login_required
def payment_done(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart= Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    
    return redirect("orders")


@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-info'})
    
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            cus=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            cus.save()
            messages.success(request,'Congratulations !! Your profile is successfully updated')
        return render(request,'app/profile.html',{'form':form,'active':'btn-info'})

@login_required
def address(request):
    addrs=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'addresses':addrs,'active':'btn-info'})


