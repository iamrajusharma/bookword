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


# home page views
def index(request):
    Products = Product.objects.all() 
    return render(request,'index.html',{'Products':Products,'user': request.user})



# add product become a seller 
@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # Handle file upload for the image
        if form.is_valid():
            form.save()
            return redirect('add_product')  # Redirect to the product list page or wherever
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

def add_to_cart(request, product_id):
    """Adds a product to the cart session or increases quantity if already present."""
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    str_product_id = str(product_id)  # Convert to string for session storage
    if str_product_id in cart:
        cart[str_product_id]['quantity'] += 1
    else:
        cart[str_product_id] = {
            'name': product.name,
            'price': str(product.price),
            'image': product.image.url,
            'quantity': 1,
        }

    request.session['cart'] = cart  # Save cart in session
    return redirect('view_cart')

def clear_cart(request, product_id):
    """Removes a specific product from the cart session."""
    cart = request.session.get('cart', {})
    str_product_id = str(product_id)

    if str_product_id in cart:
        del cart[str_product_id]
        request.session['cart'] = cart  # Save cart in session

    return redirect('view_cart')

def view_cart(request):
    """Displays the cart and calculates the total price."""

    cart = request.session.get('cart', {})  # Get cart from session
    total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())

    rupees = total_price * 86  # Replace with dynamic exchange rate if needed

    product_ids = list(cart.keys())   # Get the first product_id (if exists)

    return render(request, 'view_cart.html', {
        'cart': cart,
        'total_price': total_price,
        'rupees': rupees,
        'product_id': product_ids
    })

def add_quantity(request, product_id):
    """Increases the quantity of an item in the cart."""
    cart = request.session.get('cart', {})
    str_product_id = str(product_id)

    if str_product_id in cart:
        cart[str_product_id]['quantity'] += 1
        request.session['cart'] = cart  # Save updated cart in session

    return redirect('view_cart')

def sub_quantity(request, product_id):
    """Decreases the quantity of an item in the cart or removes it if quantity reaches 0."""
    cart = request.session.get('cart', {})
    str_product_id = str(product_id)

    if str_product_id in cart:
        if cart[str_product_id]['quantity'] > 1:
            cart[str_product_id]['quantity'] -= 1
        else:
            del cart[str_product_id]  # Remove product if quantity is 1

        request.session['cart'] = cart  # Save updated cart in session

    return redirect('view_cart')


def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        conf_password = request.POST.get('conf_password')
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('registration')
        if User.objects.filter(email=email).exists():
            messages.error(request, " Email already exists!")
            return redirect('registration')
        # Check if passwords match
        if password != conf_password:
            messages.error(request, "Passwords do not match!")
            return redirect('registration')
        # Create user
        user = User.objects.create_user(
            username=username, password=password, 
            email=email, first_name=firstname, last_name=lastname
        )
        user.save()
        # login(request, user)
    return render(request, 'registration.html')





def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  
            return redirect('index')  
        else:            
            messages.error(request, 'Invalid credentials')
    return render(request, 'user_login.html')


def user_logout(request):
    logout(request)
    return redirect('index')
    


def OrderPage(request):
    return render(request,'OrderPage.html')


