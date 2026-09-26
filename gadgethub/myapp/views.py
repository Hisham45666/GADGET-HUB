import smtplib
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User,Group
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse

from django.shortcuts import render, redirect


# Create your views here.
from myapp.models import Sellers, Customers, Categories, Complaints, Review, Product, Stock, Offers, Favourite


def logo_out(request):
    logout(request)
    return redirect('/myapp/login_get/')



def login_get(request):
    return render(request,'login.html')


def login_post(request):
    username=request.POST['username']
    password=request.POST['password']
    obj=authenticate(request,username=username,password=password)
    if obj is not None:
        login(request,obj)
        if obj.groups.filter(name="admin").exists():
            return redirect('/myapp/admin_home/')
        elif obj.groups.filter(name="customers").exists():
            return redirect('/myapp/custmers_home/')
        elif obj.groups.filter(name="sellers").exists() and Sellers.objects.filter(AUTHUSER=obj,status='Approved').exists():
            return redirect('/myapp/sellers_home/')
        else:
            messages.error(request,"invalid")
            return redirect('/myapp/login_get/')

    else:
        messages.error(request,"invalid")
        return redirect('/myapp/login_get/')


@login_required(login_url="/myapp/login_get/")
def admin_home(request):
    return render(request,'admins/index.html')

@login_required(login_url="/myapp/login_get/")
def admin_change_password(request):
    return render(request,'admins/change password.html')


@login_required(login_url="/myapp/login_get/")
def admin_change_password_post(request):
    oldpassword=request.POST['current password']
    newpassword=request.POST['new password']
    confirmpassword=request.POST['confirm password']
    data=request.user
    if data.check_password(oldpassword):
        if newpassword == confirmpassword:
            data.set_password(newpassword)
            data.save()
            return redirect('/myapp/login_get/')
        else:
            messages.error(request,"new password mismatch")
            return redirect('/myapp/admin_change_password/')
    else:
        messages.error(request, "old password mismatch")
        return redirect('/myapp/admin_change_password/')

@login_required(login_url="/myapp/login_get/")
def admin_add_category_get(request):
    return render(request,'admins/add categroy.html')

@login_required(login_url="/myapp/login_get/")
def admin_add_category_post(request):
    name=request.POST['name']

    if Categories.objects.filter(name__iexact=name).exists():
        messages.error(request, "Category already exists")
        return redirect('/myapp/admin_add_category_get/#a')

    c=Categories()
    c.name=name
    c.save()
    messages.success(request,"Added successfully")
    return redirect('/myapp/admin_viewcategory/#a')


@login_required(login_url="/myapp/login_get/")
def admin_viewcategory(request):
    data=Categories.objects.all()
    return render(request,'admins/viwe category.html',{'data':data})


@login_required(login_url="/myapp/login_get/")
def admin_edit_category(request,id):
    data=Categories.objects.get(id=id)
    return render(request,'admins/edit categroy.html',{'data':data})

@login_required(login_url="/myapp/login_get/")
def admin_edit_category_post(request):
    name = request.POST['name']
    id=request.POST['id']
    c = Categories.objects.get(id=id)
    c.name = name
    c.save()
    messages.success(request, "Updated successfully")
    return redirect('/myapp/admin_viewcategory/#a')

def admin_delete_category(request,id):
    Categories.objects.filter(id=id).delete()
    return redirect('/myapp/admin_viewcategory/')


@login_required(login_url="/myapp/login_get/")
def admin_sentreplay(request,id):
    return render(request,'admins/sentreplay.html',{'id':id})


@login_required(login_url="/myapp/login_get/")
def admin_sentreplay_post(request):
    replay=request.POST['Replay']
    id=request.POST['id']
    obj=Complaints.objects.get(id=id)
    obj.replay=replay
    obj.status="replied"
    obj.save()
    messages.success(request,"Replay Successfull")
    return redirect('/myapp/admin_viewcomplaint/#a')

@login_required(login_url="/myapp/login_get/")
def admin_view_approved_seller(request):
    data=Sellers.objects.filter(status="Approved").order_by('-id')
    return render(request,'admins/view approved sellers.html',{'data':data})

@login_required(login_url="/myapp/login_get/")
def admin_view_products(request):
    return render(request,'admins/view products.html')

@login_required(login_url="/myapp/login_get/")
def admin_view_users(request):
    data=Customers.objects.all().order_by('-id')
    return render(request,'admins/view users.html',{'data':data})

@login_required(login_url="/myapp/login_get/")
def admin_viewcomplaint(request):
    data=Complaints.objects.all().order_by('-id')
    return render(request,'admins/viewcomplaint.html',{'data':data})


@login_required(login_url="/myapp/login_get/")
def admin_viewreviews(request):
    data=Review.objects.all().order_by('-id')
    return render(request,'admins/viewreviwes.html',{'data':data})



@login_required(login_url="/myapp/login_get/")
def admin_viewsellers_and_approve_reject(request):
    data=Sellers.objects.filter(status="pending").order_by('-id')
    return render(request,'admins/viewsellers and apprve reject.html',{'S1':data})

@login_required(login_url="/myapp/login_get/")
def admin_approve_sellers(request,id):
    obj=Sellers.objects.get(id=id)
    obj.status="Approved"
    obj.save()
    messages.success(request,"approve successfull")
    return redirect("/myapp/admin_viewsellers_and_approve_reject/#a")

@login_required(login_url="/myapp/login_get/")
def admin_reject_sellers(request,id):
    obj=Sellers.objects.get(id=id)
    obj.status="Rejected"
    obj.save()
    messages.success(request,"reject successfull")
    return redirect("/myapp/admin_viewsellers_and_approve_reject/#a")




@login_required(login_url="/myapp/login_get/")
def admin_view_product(request,id):
    data=Sellers.objects.get(id=id)
    data1=Product.objects.filter(SELLERS_id=data).order_by('-id')
    return render(request,"admins/view products.html",{'data':data1} )

@login_required(login_url="/myapp/login_get/")
def admin_view_stock_get(request,id):
    b = Product.objects.get(id=id)
    a = Stock.objects.filter(PRODUCT_id=b)
    return render(request,'admins/View stock.html',{'data':a} )



##############sellers
def sellers_register_get(request):
    return render(request,'seller/sellersignup.html')

def sellers_register_post(request):
    name=request.POST['name']
    email=request.POST['email']
    phoneno=request.POST['phone']
    licenseno=request.POST['licience number']
    place=request.POST['place']
    pincode=request.POST['pincode']
    district=request.POST['district']
    state=request.POST['state']
    Latitude=request.POST['latitude']
    Longtitude=request.POST['longtitude']
    Password=request.POST['password']
    logo=request.FILES['logo']

    if User.objects.filter(username=email).exists():
        messages.error(request, "username already exists")
        return redirect('/myapp/sellers_register_get/')
    else:
        user=User.objects.create_user(username=email,password=Password)
        user.groups.add(Group.objects.get(name="sellers"))
        user.save()

        date=datetime.now().strftime("%Y%m%d-%H%M%S")+".jpeg"
        fs=FileSystemStorage()
        fs.save(date,logo)
        path=fs.url(date)


        obj=Sellers()
        obj.name=name
        obj.email=email
        obj.phone=phoneno
        obj.license_no=licenseno
        obj.place=place
        obj.pincode=pincode
        obj.district=district
        obj.state=state
        obj.latitude=Latitude
        obj.longtitude=Longtitude
        obj.logo=path
        obj.status="pending"
        obj.AUTHUSER=user
        obj.save()

        messages.success(request,"registration successfull")
        return redirect("/myapp/login_get/")



@login_required(login_url="/myapp/login_get/")
def sellers_home(request):
    return render(request,"seller/index.html")


@login_required(login_url="/myapp/login_get/")
def seller_profile(request):
    data=Sellers.objects.get(AUTHUSER=request.user)
    return render(request,"seller/viewprofile.html",{'data':data} )


@login_required(login_url="/myapp/login_get/")
def seller_edit_profile_get(request):
    data=Sellers.objects.get(AUTHUSER=request.user)
    return render(request,"seller/editprofile.html",{'data':data})

@login_required(login_url="/myapp/login_get/")
def seller_edit_profile_post(requset):
    name=requset.POST['name']
    phoneno=requset.POST['phone number']
    licenseno=requset.POST['licience number']
    place=requset.POST['place']
    pincode=requset.POST['pincode']
    district=requset.POST['district']
    state=requset.POST['state']
    latitude=requset.POST['latitude']
    longtitude=requset.POST['longtitude']

    obj=Sellers.objects.get(AUTHUSER=requset.user)
    obj.name=name
    obj.phone=phoneno
    obj.pincode=pincode
    obj.district=district
    obj.state=state
    obj.license_no=licenseno
    obj.latitude=latitude
    obj.place=place
    obj.longtitude=longtitude

    if 'logo' in requset.FILES:
        logo=requset.FILES['logo']
        if logo != "":
            date = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpeg"
            fs = FileSystemStorage()
            fs.save(date, logo)
            path = fs.url(date)
            obj.logo=path
            obj.save()

    obj.save()
    messages.success(requset,'Edit successfully')
    return redirect("/myapp/seller_profile/#a")


@login_required(login_url="/myapp/login_get/")
def seller_add_product_get(request):
    data=Categories.objects.all()
    return render(request,"seller/add product.html",{'data':data})

@login_required(login_url="/myapp/login_get/")
def seller_add_product_post(request):
    name=request.POST['name']
    discrpition=request.POST['discrpition']
    price=request.POST['price']
    photo=request.FILES['photo']
    category=request.POST['category']

    date = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpeg"
    fs = FileSystemStorage()
    fs.save(date,photo)
    path = fs.url(date)

    obj=Product()
    obj.name=name
    obj.discription=discrpition
    obj.price=price
    obj.CATEGORIES_id=category
    obj.photo=path
    obj.SELLERS=Sellers.objects.get(AUTHUSER=request.user)
    obj.save()
    messages.success(request,'Added successfully')
    return redirect("/myapp/sellers_view_product_get/#a")


@login_required(login_url="/myapp/login_get/")
def sellers_view_product_get(request):
    data=Product.objects.filter(SELLERS__AUTHUSER=request.user)
    return render(request,'seller/view product.html',{'data':data})

@login_required(login_url="/myapp/login_get/")
def sellers_delete_product(request,id):
    Product.objects.filter(id=id).delete()
    messages.success(request,"Delete success")
    return redirect("/myapp/sellers_view_product_get/")

def sellers_edit_product_get(request,id):
    data=Product.objects.get(id=id)
    data2=Categories.objects.all()
    return render(request,"seller/edit product.html",{'data':data,'data2':data2})


@login_required(login_url="/myapp/login_get/")
def sellers_edit_product_post(request):
    id=request.POST['id']
    name = request.POST['name']
    discrpition = request.POST['discrpition']
    price = request.POST['price']
    category = request.POST['category']

    obj=Product.objects.get(id=id)




    if 'photo' in request.FILES:
        photo=request.FILES['photo']
        date = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpeg"
        fs = FileSystemStorage()
        fs.save(date, photo)
        path = fs.url(date)
        obj.logo = path
        obj.save()

    obj.name = name
    obj.discription = discrpition
    obj.price = price
    obj.CATEGORIES_id = category
    obj.save()
    messages.success(request,'Edit scccesss')
    return redirect("/myapp/sellers_view_product_get/#a")


@login_required(login_url="/myapp/login_get/")
def sellers_add_stock_get(request,id):
    a=Product.objects.get(id=id)
    return render(request,'seller/add stock.html',{'data':a})
@login_required(login_url="/myapp/login_get/")
def sellers_add_stock_post(request):
    id = request.POST['id']
    stock = int(request.POST['stock'])

    a = Stock.objects.filter(PRODUCT_id=id).first()

    if a:
        a.stock += stock
        a.save()
    else:
        a = Stock()
        a.PRODUCT = Product.objects.get(id=id)
        a.stock = stock
        a.save()

    messages.success(request, 'Stock added successfully')
    return redirect("/myapp/sellers_view_product_get/#a")

@login_required(login_url="/myapp/login_get/")
def seller_view_stock_get(request,id):
    b = Product.objects.get(id=id)
    a = Stock.objects.filter(PRODUCT_id=b)
    return render(request,'seller/View stock.html',{'data':a} )




# def sellers_add_offer_get(request,id):
#     a=Product.objects.get(id=id)
#     return render(request,'seller/add offer.html',{'data':a})
#
# def sellers_add_offer_post(request):
#     id = request.POST['id']
#     offers_price = request.POST['offers_price']
#     expiry_date = request.POST['expiry_date']
#
#     a=Offers()
#     a.PRODUCT=Product.objects.get(id=id)
#     a.offers_price=offers_price
#     a.expiry_date=expiry_date
#     a.save()
#     messages.success(request, 'Offer Added scccesss')
#     return redirect("/myapp/sellers_view_product_get/#a")
#
# def sellers_edit_offer_get(request,id):
#     a=Offers.objects.get(id=id)
#     return render(request,'seller/edit offer.html',{'data':a})
#
# def sellers_edit_offer_post(request):
#     id = request.POST['id']
#     offers_price = request.POST['offers_price']
#     expiry_date = request.POST['expiry_date']
#
#     a=Offers.objects.get(id=id)
#     a.offers_price=offers_price
#     a.expiry_date=expiry_date
#     a.save()
#     messages.success(request, 'Edit scccesss')
#     return redirect("/myapp/sellers_view_product_get/#a")


@login_required(login_url="/myapp/login_get/")
def sellers_add_offer_get(request, id):
    product = Product.objects.get(id=id)

    active_offer = Offers.objects.filter(
        PRODUCT=product,
        expiry_date__gte=timezone.now().date()
    ).first()

    if active_offer:
        messages.warning(
            request,
            'This product already has an active offer until ' +
            str(active_offer.expiry_date)
        )
        return redirect("/myapp/sellers_view_product_get/#a")

    return render(
        request,
        'seller/add offer.html',
        {'data': product}
    )


@login_required(login_url="/myapp/login_get/")
def sellers_add_offer_post(request):
    id = request.POST['id']
    offers_price = request.POST['offers_price']
    expiry_date = request.POST['expiry_date']

    product = Product.objects.get(id=id)

    active_offer = Offers.objects.filter(
        PRODUCT=product,
        expiry_date__gte=timezone.now().date()
    ).first()

    if active_offer:
        messages.warning(
            request,
            'This product already has an active offer.'
        )
        return redirect("/myapp/sellers_view_product_get/#a")

    offer = Offers()
    offer.PRODUCT = product
    offer.offers_price = offers_price
    offer.expiry_date = expiry_date
    offer.save()

    messages.success(request, 'Offer Added Successfully')

    return redirect("/myapp/sellers_view_product_get/#a")


@login_required(login_url="/myapp/login_get/")
def sellers_edit_offer_get(request, id):
    offer = Offers.objects.get(id=id)

    return render(
        request,
        'seller/edit offer.html',
        {'data': offer}
    )


@login_required(login_url="/myapp/login_get/")
def sellers_edit_offer_post(request):
    id = request.POST['id']
    offers_price = request.POST['offers_price']
    expiry_date = request.POST['expiry_date']

    offer = Offers.objects.get(id=id)

    offer.offers_price = offers_price
    offer.expiry_date = expiry_date
    offer.save()

    messages.success(request, 'Offer Edited Successfully')

    return redirect("/myapp/sellers_view_product_get/#a")

@login_required(login_url="/myapp/login_get/")
def admin_delete_offers(request,id):
    Offers.objects.filter(id=id).delete()
    messages.success(request, 'Delete scccesss')
    return redirect('/myapp/sellers_view_product_get/')


@login_required(login_url="/myapp/login_get/")
def seller_view_offers_get(request,id):
    b = Product.objects.get(id=id)
    a = Offers.objects.filter(PRODUCT_id=b)
    return render(request,'seller/view offers.html',{'data':a} )






@login_required(login_url="/myapp/login_get/")
def sellers_edit_stock_get(request,id):
    a=Stock.objects.get(id=id)
    return render(request,'seller/edit stock.html',{'data':a})

@login_required(login_url="/myapp/login_get/")
def sellers_edit_stock_post(request):
    id = request.POST['id']
    stock = request.POST['stock']

    a=Stock.objects.get(id=id)
    a.stock=stock
    a.save()
    messages.success(request, 'Edit scccesss')
    return redirect("/myapp/sellers_view_product_get/#a")


@login_required(login_url="/myapp/login_get/")
def seller_view_compliant_replay(request):
    data=Complaints.objects.filter(AUTHUSER_id=request.user)
    return render(request,'seller/view replay.html',{'data':data})

@login_required(login_url="/myapp/login_get/")
def seller_sent_compliant_get(request):
    return render(request,'seller/sent complient.html')

def seller_sent_complaint(request):
    complaint = request.POST['complaint']

    a=request.user


    a=Complaints()
    a.compliant=complaint
    a.date=datetime.now().today()
    a.replay="pending"
    a.status="pending"
    a.AUTHUSER = request.user
    a.save()
    messages.success(request, 'Complaint Sent')
    return redirect("/myapp/seller_view_compliant_replay/#a")




@login_required(login_url="/myapp/login_get/")
def seller_sent_review(request):
    review = request.POST['review']

    a = Review()
    a.review = review
    a.date = datetime.now().date()
    a.AUTHUSER = request.user
    a.save()
    messages.success(request, 'Sent Review scccesss')

    return redirect("/myapp/sellers_home/#a")


@login_required(login_url="/myapp/login_get/")
def seller_sent_review_get(request):
    return render(request,'seller/sent review.html')


@login_required(login_url="/myapp/login_get/")
def seller_change_password(request):
    return render(request,'seller/change password.html')


@login_required(login_url="/myapp/login_get/")
def seller_change_password_post(request):
    oldpassword=request.POST['current_password']
    newpassword=request.POST['new_password']
    confirmpassword=request.POST['confirm_password']
    data=request.user
    if data.check_password(oldpassword):
        if newpassword == confirmpassword:
            data.set_password(newpassword)
            data.save()
            return redirect('/myapp/login_get/')
        else:
            messages.error(request,"new password mismatch")
            return redirect('/myapp/seller_change_password_get/')
    else:
        messages.error(request, "old password mismatch")
        return redirect('/myapp/seller_change_password_get/')



###################users



def user_singup(request):
    return render(request,"users/signup.html")

def user_signup_post(request):
    name=request.POST['name']
    gender=request.POST['gender']
    place=request.POST['place']
    pincode=request.POST['pincode']
    state=request.POST['state']
    district=request.POST['district']
    password=request.POST['password']
    cpassword=request.POST['confirm password']
    email=request.POST['email']
    phone=request.POST['phone']

    if User.objects.filter(username=email).exists():
        messages.error(request, "username already exists")
        return redirect('/myapp/sellers_register_get/')
    else:
        user=User.objects.create_user(username=email,password=password)
        user.groups.add(Group.objects.get(name="customers"))
        user.save()

        c=Customers()
        c.name=name
        c.email=email
        c.phone=phone
        c.gender=gender
        c.place=place
        c.pincode=pincode
        c.state=state
        c.district=district
        c.AUTHUSER=user
        c.save()
        messages.success(request, "registration successfull")
        return redirect("/myapp/login_get/")



@login_required(login_url="/myapp/login_get/")
def custmers_home(request):
    return render(request,'users/index.html')
@login_required(login_url="/myapp/login_get/")
def customers_profile(request):
    data=Customers.objects.get(AUTHUSER=request.user)
    return render(request,"users/view profile.html",{'data':data} )


@login_required(login_url="/myapp/login_get/")
def customers_edit_profile_get(request):
    data=Customers.objects.get(AUTHUSER=request.user)
    return render(request,"users/edit profile.html",{'data':data})

@login_required(login_url="/myapp/login_get/")
def customers_edit_profile_post(request):
    name = request.POST['name']
    gender = request.POST['gender']
    place = request.POST['place']
    pincode = request.POST['pincode']
    state = request.POST['state']
    district = request.POST['district']
    email = request.POST['email']
    phone = request.POST['phone']


    c = Customers.objects.get(AUTHUSER=request.user)
    c.name = name
    c.email = email
    c.phone = phone
    c.gender = gender
    c.place = place
    c.pincode = pincode
    c.state = state
    c.district = district
    c.save()
    messages.success(request, "Edited successfull")
    return redirect("/myapp/customers_profile/")


# def customers_view_near_by_sellers(request):
#
#
#     data=Sellers.objects.filter(status="Approved")
#     return render(request,"users/viewsellers.html",{'data':data} )


import math


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def customers_view_near_by_sellers(request):
    user_lat = request.GET.get("latitude")
    user_lon = request.GET.get("longitude")

    nearby_sellers = []

    if user_lat and user_lon:

        try:
            user_lat = float(user_lat)
            user_lon = float(user_lon)
            sellers = Sellers.objects.filter(status="Approved")
            for seller in sellers:

                try:
                    seller_lat = float(seller.latitude)
                    seller_lon = float(seller.longtitude)
                    distance = calculate_distance(
                        user_lat,
                        user_lon,
                        seller_lat,
                        seller_lon
                    )
                    if distance <= 5:
                        seller.distance = round(distance, 2)
                        nearby_sellers.append(seller)

                except (ValueError, TypeError):
                    continue

        except (ValueError, TypeError):
            pass

    return render(request,"users/viewsellers.html",{"data": nearby_sellers})


# def customers_view_near_by_sellers(request):
#     customer = Customers.objects.get(AUTHUSER=request.user)
#
#     data = Sellers.objects.filter(
#         status="Approved",
#         pincode=customer.pincode
#     )
#
#     return render(request, "users/viewsellers.html", {'data': data})

# def customers_product(request,id):
#     data=Sellers.objects.get(id=id)
#     data1=Product.objects.filter(SELLERS_id=data)
#     return render(request,"users/view product.html",{'data':data1} )


def customers_product(request, id):
    products = Product.objects.filter(
        SELLERS_id=id
    ).select_related(
        'CATEGORIES',
        'SELLERS'
    ).prefetch_related(
        'stock_set',
        'offers_set'
    )

    user_favorites = Favourite.objects.filter(
        AUTHUSER=request.user
    ).values_list('PRODUCT_id', flat=True)

    return render(request, "users/view product.html", {
        'products': products,
        'user_favorites': user_favorites
    })


@login_required(login_url="/myapp/login_get/")
def customers_view_compliant_replay(request):
    data=Complaints.objects.filter(AUTHUSER_id=request.user)
    return render(request,'users/view replay.html',{'data':data})

@login_required(login_url="/myapp/login_get/")
def customers_sent_complaint(request):
    complaint = request.POST['complaint']

    # a=request.user


    a=Complaints()
    a.compliant=complaint
    a.date=datetime.now().today()
    a.replay="pending"
    a.status="pending"
    a.AUTHUSER = request.user
    a.save()
    return redirect("/myapp/customers_view_compliant_replay/#a")

@login_required(login_url="/myapp/login_get/")
def customers_sent_compliant_get(request):
    return render(request,'users/sent complient.html')


@login_required(login_url="/myapp/login_get/")
def customers_sent_review(request):
    review = request.POST['review']

    a = Review()
    a.review = review
    a.date = datetime.now().date()
    a.AUTHUSER = request.user
    a.save()

    return redirect("/myapp/custmers_home/#a")


@login_required(login_url="/myapp/login_get/")
def customers_sent_review_get(request):
    return render(request,'users/sent review.html')


@login_required(login_url="/myapp/login_get/")
def customers_change_password(request):
    return render(request,'users/change password.html')


@login_required(login_url="/myapp/login_get/")
def customers_change_password_post(request):
    oldpassword=request.POST['current_password']
    newpassword=request.POST['new_password']
    confirmpassword=request.POST['confirm_password']
    data=request.user
    if data.check_password(oldpassword):
        if newpassword == confirmpassword:
            data.set_password(newpassword)
            data.save()
            return redirect('/myapp/login_get/')
        else:
            messages.error(request,"new password mismatch")
            return redirect('/myapp/customers_change_password/')
    else:
        messages.error(request, "old password mismatch")
        return redirect('/myapp/customers_change_password/')


def add_Favourite(request,id):

    a=Favourite()
    a.AUTHUSER=request.user
    a.PRODUCT=Product.objects.get(id=id)
    a.save()
    return redirect('/myapp/customers_view_near_by_sellers/')



# def customers_view_favourates(request):
#     favourites = Favourite.objects.filter(AUTHUSER=request.user)
#
#     data = Product.objects.filter(
#         id__in=favourites.values_list('PRODUCT_id', flat=True)
#     )
#
#     return render(
#         request,
#         'users/view product_favouratis.html',
#         {'data': data}
#     )


def customers_view_favourates(request):
    favourites = Favourite.objects.filter(AUTHUSER=request.user)

    products = Product.objects.filter(
        id__in=favourites.values_list('PRODUCT_id', flat=True)
    ).select_related(
        'CATEGORIES',
        'SELLERS'
    ).prefetch_related(
        'stock_set',
        'offers_set'
    )

    user_favorites = favourites.values_list('PRODUCT_id', flat=True)

    return render(request,'users/view product_favouratis.html',{'products': products,'user_favorites': user_favorites})


def customers_delete_favourites(request, id):
    Favourite.objects.filter(
        AUTHUSER=request.user,
        PRODUCT_id=id
    ).delete()

    return redirect('/myapp/customers_view_favourates/#a')





#
from django.utils import timezone

def customers_view_product(request):

    products = Product.objects.select_related(
        'CATEGORIES',
        'SELLERS'
    ).prefetch_related(
        'stock_set',
        'offers_set'
    ).all()

    user_favorites = Favourite.objects.filter(
        AUTHUSER=request.user
    ).values_list(
        'PRODUCT_id',
        flat=True
    )

    today = timezone.now().date()

    for product in products:

        latest_offer = product.offers_set.order_by(
            '-expiry_date'
        ).first()

        product.latest_offer = latest_offer

        if latest_offer:

            if latest_offer.expiry_date >= today:
                product.offer_active = True
            else:
                product.offer_active = False

        else:
            product.offer_active = False

    context = {
        'products': products,
        'user_favorites': user_favorites,
    }

    return render(
        request,
        "users/view products.html",
        context
    )

def toggle_favorite(request, product_id):
    if request.method == "POST":
        customer = Customers.objects.get(AUTHUSER=request.user)
        product = Product.objects.get(id=product_id)

        fav_exists = Favourite.objects.filter(AUTHUSER=request.user, PRODUCT=product).exists()

        if fav_exists:
            Favourite.objects.filter(AUTHUSER=request.user, PRODUCT=product).delete()
            return JsonResponse({'status': 'success', 'action': 'removed'})
        else:
            Favourite.objects.create(AUTHUSER=request.user, PRODUCT=product)
            return JsonResponse({'status': 'success', 'action': 'added'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def get_actual_price(product):
    offer = product.offers_set.first()
    try:
        if offer:
            return float(offer.offers_price)
        else:
            return float(product.price)
    except ValueError:
        return 0.0


# def compare_product(request, product_id):
#     # 1. Get the product the user clicked on
#     try:
#         selected_product = Product.objects.select_related(
#             'CATEGORIES', 'SELLERS'
#         ).prefetch_related(
#             'offers_set', 'stock_set'
#         ).get(id=product_id)
#
#     except Product.DoesNotExist:
#         # If the product doesn't exist in the database, show a simple error message
#         return HttpResponse("Sorry, this product could not be found.")
#
#     sel_price = get_actual_price(selected_product)
#
#     # 3. Find other products in the exact same category (excluding the selected one)
#     other_products = Product.objects.filter(
#         CATEGORIES=selected_product.CATEGORIES
#     ).exclude(
#         id=selected_product.id
#     ).select_related('CATEGORIES', 'SELLERS').prefetch_related('offers_set')
#
#     # 4. Filter the list to only include products that are cheaper
#     cheaper_products = []
#
#     for product in other_products:
#         product_price = get_actual_price(product)
#
#         if product_price < sel_price:
#             product.effective_price = product_price
#             product.savings = sel_price - product_price
#             cheaper_products.append(product)
#
#     cheaper_products.sort(key=lambda x: x.effective_price)
#
#     user_favorites = []
#     # customer = Customers.objects.get(AUTHUSER=request.user)
#     user_favorites = Favourite.objects.filter(AUTHUSER=request.user).values_list('PRODUCT_id', flat=True)
#
#     context = {
#         'selected_product': selected_product,
#         'sel_price': sel_price,
#         'similar_products': cheaper_products,
#         'user_favorites': user_favorites
#     }
#
#     return render(request, 'users/compare_products.html', context)


def compare_product(request, product_id):

    today = timezone.now().date()

    try:
        selected_product = Product.objects.select_related(
            'CATEGORIES',
            'SELLERS'
        ).prefetch_related(
            'offers_set',
            'stock_set'
        ).get(id=product_id)

    except Product.DoesNotExist:
        return HttpResponse("Sorry, this product could not be found.")

    # -----------------------------------
    # SELECTED PRODUCT
    # -----------------------------------

    # Get offer with latest expiry date
    latest_offer = selected_product.offers_set.order_by(
        '-expiry_date'
    ).first()

    # Check whether offer is still active
    if latest_offer and latest_offer.expiry_date >= today:
        selected_product.offer = latest_offer
    else:
        selected_product.offer = None

    selected_product.stock_info = selected_product.stock_set.first()

    # Get actual price
    sel_price = get_actual_price(selected_product)


    # -----------------------------------
    # OTHER PRODUCTS IN SAME CATEGORY
    # -----------------------------------

    other_products = Product.objects.filter(
        CATEGORIES=selected_product.CATEGORIES
    ).exclude(
        id=selected_product.id
    ).select_related(
        'CATEGORIES',
        'SELLERS'
    ).prefetch_related(
        'offers_set',
        'stock_set'
    )


    cheaper_products = []


    for product in other_products:

        # Get latest offer based on expiry date
        latest_offer = product.offers_set.order_by(
            '-expiry_date'
        ).first()

        # Only use offer if it is not expired
        if latest_offer and latest_offer.expiry_date >= today:
            product.offer = latest_offer
        else:
            product.offer = None

        # Get stock
        product.stock_info = product.stock_set.first()

        # Get actual/effective price
        product_price = get_actual_price(product)


        # Only products cheaper than selected product
        if product_price < sel_price:

            product.effective_price = product_price

            product.savings = sel_price - product_price

            cheaper_products.append(product)


    # Sort cheapest first
    cheaper_products.sort(
        key=lambda x: x.effective_price
    )


    # -----------------------------------
    # USER FAVORITES
    # -----------------------------------

    user_favorites = Favourite.objects.filter(
        AUTHUSER=request.user
    ).values_list(
        'PRODUCT_id',
        flat=True
    )


    # -----------------------------------
    # CONTEXT
    # -----------------------------------

    context = {
        'selected_product': selected_product,
        'sel_price': sel_price,
        'similar_products': cheaper_products,
        'user_favorites': user_favorites
    }


    return render(
        request,
        'users/compare_products.html',
        context
    )










def forget_password_get(request):
    return render(request,'forgetpassword.html')

def forget_password_post(request):
    if request.method == 'POST':
        email = request.POST.get('username','').strip()
        try:
            user=User.objects.get(username=email)
        except User.DoesNotExist:
            messages.warning(request,'Email does not exist')
            return redirect('/myapp/login_get/')
        import random
        psw = random.randint(1000,9999)

        user.set_password(str(psw))
        user.save()

        try:
            server=smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('trainingstarted@gmail.com', 'nlxasujxgazlbmgz')

            subject = "Password Reset - Construction App"
            body = "Your new password is: "+str(psw)
            msg = f"Subject: {subject}\n\n{body}"

            server.sendmail("trainingstarted@gmail.com",email, msg)
            server.quit()

            messages.success(request,'Password Send Successfuly')
            return  redirect('/myapp/login_get/')
        except Exception as e:
            messages.warning(request,'Faild to Send')
            return  redirect('/myapp/login_get/')


    messages.warning(request,'Faild to Send')
    return redirect('/myapp/login_get')



