from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from catalog.models import Account, Customer, Restaurant, Rider, Food, Order
from catalog import forms
from cart.cart import Cart
import hashlib

# Create your views here.


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def index(request):
    index_form = forms.IndexForm()
    rest_list = Restaurant.objects.all().exclude(RName__isnull=True)
    if not request.session.get('is_login', None):
        return redirect('/login/')
    context = {
        'index_form': index_form,
        'rest_list': rest_list
    }

    return render(request, 'index.html', context=context)


def restaurant_detail(request, pk):
    restaurant_info = get_object_or_404(Restaurant, pk=pk)
    food_list = Food.objects.filter(RName=restaurant_info.RName)
    request.session["current_url"] = 

    context = {
        'restaurant_info': restaurant_info,
        'food_list': food_list
    }

    return render(request, 'restaurant_detail.html', context)


def add_to_cart(request, food_id):
    print('ok')
    food = Food.objects.get(food_id=food_id)
    cart = Cart(request)
    cart.add(food, food.price, quantity=1)
    return redirect('/')

def remove_from_cart(request, food_id):
    food = Food.objects.get(food_id=food_id)
    cart = Cart(request)
    cart.remove(food)
    return redirect('/index/cart/')

def get_cart(request):
    return render(request, 'cart.html', {'cart': Cart(request)})


def login(request):
    login_form = forms.LoginForm()
    message = ''
    redirect_page = ''

    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')

    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = Account.objects.get(AName=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_name'] = user.AName
                    request.session['account_type'] = user.account_type
                    if user.account_type == 'customer':
                        customer = Customer.objects.get(AName_id=user.AName)
                        request.session['address'] = customer.address
                        redirect_page = '/index/'
                    elif user.account_type == 'restaurant':
                        redirect_page = '/restaurant/'
                    elif user.account_type == 'rider':
                        redirect_page = '/rider/'
                    return redirect(redirect_page)
                else:
                    message = '密码错误!'
            except:
                message = '用户不存在!'
        else:
            message = '请正确填写内容!'

    context = {
        'login_form': login_form,
        'message': message
    }

    return render(request, 'login.html', context=context)


def register(request):
    register_form = forms.RegisterForm()
    message = ''

    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get('password')
            confirm_pw = register_form.cleaned_data.get('confirm_pw')
            sex = register_form.cleaned_data.get('sex')
            last_name = register_form.cleaned_data.get('last_name')
            first_name = register_form.cleaned_data.get('first_name')
            birth = register_form.cleaned_data.get('birth')
            email = register_form.cleaned_data.get('email')
            personal_ID = register_form.cleaned_data.get('personal_ID')
            phone = register_form.cleaned_data.get('phone')
            role = register_form.cleaned_data.get('role')

            if password != confirm_pw:
                message = '两次密码不同!'
            else:
                sanme_name_user = Account.objects.filter(AName=username)
                same_email_user = Account.objects.filter(email=email)
                same_phone_user = Account.objects.filter(phone=phone)
                same_personal_ID_user = Account.objects.filter(personal_ID=personal_ID)
                if sanme_name_user:
                    message = '账户已存在'
                elif same_email_user:
                    message = '邮箱已存在'
                elif same_phone_user:
                    message = '手机号已存在'
                elif same_personal_ID_user:
                    message = '身份证已存在'
                else:
                    new_user = Account()
                    new_user.AName = username
                    new_user.password = hash_code(password)
                    new_user.sex = sex
                    new_user.last_name = last_name
                    new_user.first_name = first_name
                    new_user.birth = birth
                    new_user.email = email
                    new_user.personal_ID = personal_ID
                    new_user.phone = phone
                    new_user.account_type = role
                    new_user.save()
                    if new_user.account_type == 'customer':
                        new_customer = Customer()
                        new_customer.AName_id = username
                        new_customer.save()
                    elif new_user.account_type == 'restaurant':
                        new_restaurant = Restaurant()
                        new_restaurant.AName_id = username
                        new_restaurant.save()
                    elif new_user.account_type == 'rider':
                        new_rider = Rider()
                        new_rider.AName_id = username
                        new_rider.save()
                    
                    return redirect('/login/')

    context = {
        'register_form': register_form,
        'message': message
    }

    return render(request, 'register.html', context=context)


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    request.session.flush()

    return redirect('/login/')


def get_password(request):
    pass
    return render(request, 'get_password.html')


def restaurant(request):
    pass
    return render(request, 'restaurant.html')


def rider(request):
    pass
    return render(request, 'rider.html')