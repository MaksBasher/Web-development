from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify

# Create your models here.

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

ITEM_STATUS = (
    (0,"Out of Stock"),
    (1,"In Stock")
)

class News(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    image = models.ImageField(upload_to="images/%Y/%m/%d/", null=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = "News"
    def __str__(self):
        return self.title
   
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    phone = PhoneNumberField(null=False, blank=False, unique=True)

    def __str__(self):
	    return self.name

#class Inventory(models.Model):
    #inventory_id = models.AutoField(primary_key=True)
    #quantity = models.IntegerField()
    #created_on = models.DateTimeField(auto_now_add=True)
    #updated_on = models.DateTimeField(auto_now= True)
    
    #class Meta:
        #verbose_name_plural = "Inventories"
    
class Discount(models.Model):
    discount_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    discount_amount = models.DecimalField(max_digits=3, decimal_places=2)
    active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now= True)
    
    class Meta:
        ordering = ['discount_id']
    
    def __str__(self):
            return self.name

class Product_Category (models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now= True)
    
    class Meta:
        verbose_name_plural = "Product Categories"
        ordering = ['category_id']
        
    def __str__(self):
        # Return a string that represents the instance
        return f"{self.category_name}"

class Brand (models.Model):
    brand_id = models.AutoField(primary_key=True)
    logo = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now= True)
    
    class Meta:
        ordering = ['brand_id']
    
    def __str__(self):
        # Return a string that represents the instance
        return f"{self.name}"
         
class Product(models.Model):
    brand = models.ForeignKey(Brand,null=True, on_delete= models.CASCADE)
    product_id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="images/%Y/%m/%d/", null=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length = 250, null = True, blank = True, unique=True)
    description = models.TextField(max_length=500)
    SKU = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Product_Category, on_delete= models.CASCADE)
    stock_status = models.IntegerField(choices=ITEM_STATUS, default=0)
    discount_id = models.ForeignKey(Discount, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now= True)
    
    class Meta:
        ordering = ['product_id']
    
    def __str__(self):
        return self.name
    
    #auto slug
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	ordered_on = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	created_on = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    country = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    address = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    
    class Meta:
        verbose_name_plural = "ShippingAddress"