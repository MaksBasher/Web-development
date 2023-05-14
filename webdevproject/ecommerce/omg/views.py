import json
from django.shortcuts import  render, redirect, get_object_or_404
from django.views import generic
from .models import *
from django import forms
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth import login, authenticate 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views import View

# Create your views here.

#Home page views
def index(request):
    my_dict = {"insert_me": "I am from views.py"}
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
    context = {'products': products, 
               'discounts': discounts,}
    return render(request, 'category.html', context)

#Items views
class ProductView(generic.DetailView):
    model = Product
    template_name = 'item.html'
    context_object_name = 'product'

#Tracking views
def tracking(request):
     context = {}
     return render(request, 'tracking.html', context)
     
#Cart views
def cart(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0}
        
    context = {'items':items,
               'order':order}
    return render(request, 'cart.html', context)

def updateItem(request):
    data = json.loads(request.data)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)
    return JsonResponse('Item was added', safe=False)

#Checkout views    
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0}
        
    context = {'items':items,
               'order':order}
    return render(request, 'checkout.html', context)
 
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
            return redirect("omg:home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="register.html", context={"register_form":form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {email}.")
                return redirect("omg:home")
            else:
                messages.error(request,"Invalid email or password.")
        else:
            messages.error(request,"Invalid email or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})