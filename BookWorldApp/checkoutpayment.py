from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import ProductForm
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Product
from django.contrib.auth import logout




def CheckoutPage(request):
    # Get cart data from the session
    cart = request.session.get('cart', {})
    
    products = []
    product_ids = []  # Initialize an empty list for product IDs
    
    for product_id, quantity in cart.items():
        # Get the product object
        product = Product.objects.get(id=product_id)
        
        # Append the product and its quantity to the products list
        products.append({'product': product, 'quantity': quantity})
        
        # Append the product ID to the product_ids list
        product_ids.append(str(product.id))  # Ensure the ID is a string
    
    # Join the product IDs into a comma-separated string
    product_ids_str = ",".join(product_ids)

    # Prepare context
    context = {
        'products': products,
        'product_ids': product_ids_str  # Pass the comma-separated product IDs string
    }
    
    return render(request, 'CheckoutPage.html', context)




# views.py

# def CheckoutPage(request, product_id):
#     cart = request.session.get('cart', {})  # Get cart from session
#     context = {
#         'product_id': product_id,  # Pass product_id to template
#     }
#     return render(request, 'checkout.html', context)
