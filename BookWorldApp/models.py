from django.db import models

# Create your models here.


from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    Quantity = models.IntegerField(blank=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    author = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    def __str__(self):
        return self.name

class Register(models.Model):
    username=models.CharField(max_length=50)
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    email=models.EmailField()
    password=models.CharField(max_length=50)
  
    def __str__(self):
        return self.username

    

from django.db import models

class PaymentModel(models.Model):
    Product_name = models.TextField()  # TEXT is sufficient here
    Product_id = models.TextField()    # TEXT is sufficient here
    amount = models.DecimalField(max_digits=8, decimal_places=2)  # Keep a reasonable size
    created_at = models.DateTimeField(auto_now_add=True)
    currency = models.CharField(max_length=3)  # Short length for currency
    order_id = models.CharField(max_length=150)  # Adjusted for a reasonable size
    status = models.CharField(max_length=50)  # Adjusted for reasonable length

    def __str__(self):
        return f"Order {self.order_id} - Status: {self.status}"
