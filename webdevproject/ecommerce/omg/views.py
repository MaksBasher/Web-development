import datetime
from django.shortcuts import  get_object_or_404, render, redirect
from django.views import generic
from .models import *
from django import forms
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
import json
from .utils import *

# Create your views here.

#Home page views
def index(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0}
        cartItems = order['get_cart_items']
        
    my_dict = {'items':items,
               'order':order,
               'cartItems': cartItems,
               'products':products}
    return render(request,'index.html',context=my_dict)

#News views 
class NewsList(generic.ListView):
    queryset = News.objects.filter(status=1).order_by('-created_on')
    template_name = "news.html"

class NewsDetail(generic.DetailView):
    model = News
    template_name = "news_detail.html"
    
#Categories views 
def category(request):  
    products = Product.objects.all()
    discounts = Discount.objects.all()
    brands = Brand.objects.all()
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0}
        cartItems = order['get_cart_items'] 
    context = {'products': products, 
               'discounts': discounts,
               'cartItems': cartItems,
               'order':order,
               'items':items,
               'brands':brands
               }
    return render(request, 'category.html', context)


def fav_item (request, id):
    product = get_object_or_404(Product, id=id)
    if product.favorite.filter(id=request.user.id).exists():
        product.favorite.remove(request.user)
    else:
        product.favorite.add(request.user)
    return HttpResponseRedirect(product.get_absolute_url())


#Items views
class ProductView(generic.DetailView):
    model = Product
    template_name = 'item.html'
    context_object_name = 'product'
#def item(request, slug):
    #products = Product.objects.all()
    #discounts = Discount.objects.all()
    #context = {'products': products, 
    #           'discounts': discounts,
    #           "slug": slug}
    #return render(request, 'item.html', context)

def updateItem(request):
    data = json.loads (request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)
    
    customer = request.user
    product = Product.objects.get(product_id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse ('Item was added', safe=False)


#Tracking views
def tracking(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
        
    context = {'cartItems':cartItems ,'order':order, 'items':items}
    return render(request, 'tracking.html', context)
     
#Cart views
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
        
    context = {'cartItems':cartItems ,'order':order, 'items':items}
    return render(request, 'cart.html', context)

#Checkout views    
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
        
    context = {'cartItems':cartItems ,'order':order, 'items':items}
    return render(request, 'checkout.html', context)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    tracking_number = id_generator()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        total = data['form']['total']
        order.transaction_id = transaction_id
        order.tracking_number = tracking_number
        order.complete = True
        order.save()
        
        if order.shipping == True:
           ShippingAddress.objects.create(
               customer = request.user,
               order = order,
               address = data['shipping']['address'],
               city = data['shipping']['city'],
               state = data['shipping']['state'],
               zipcode = data['shipping']['zipcode'],
               country = data['shipping']['country']
           )
       
    else: 
        print("User not logged in..")
        
    return JsonResponse('Payment submitted..', safe=False)

#Profile page
@login_required
def profile(request):
    profile = Customer.objects.all()
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
        
    context = {'cartItems':cartItems ,'order':order, 'items':items, 'profile':profile}
    return render(request,'profile.html', context)


#Favorites page
def favorite(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0}
        cartItems = order['get_cart_items']
        
    context = {'items':items,
               'order':order,
               'cartItems': cartItems}
    return render(request,'favorite.html', context)

#User auth views
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", 
                  "email", 
                  "first_name", 
                  "last_name", 
                  "password1", 
                  "password2",
                  )

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("profile")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="register.html", context={"register_form":form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("profile")
            else:
                messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("home")

#Password reset views
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

#Test page

def testpage(request):
    return render(request,'test.html')