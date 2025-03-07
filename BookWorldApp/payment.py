import razorpay

from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from .models import Product, PaymentModel
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Initialize Razorpay Client (Make sure to replace test keys with production keys when live)
client = razorpay.Client(auth=("rzp_test_fWRIgScE7JV0Aa", "q2bHyvbyvyIrN0kL0aBTtylx"))



# def PaymentCreated(request, product_id):
#     """Create Razorpay order and save details in the database"""
#     product = get_object_or_404(Product, id=product_id)

#     product_amount = int(product.price)  # Convert price to integer (if stored as float)
#     product_name = product.name

#     data = {
#         "amount": product_amount * 100,  # Convert to paise
#         "currency": "INR",
#         "receipt": f"order_rcptid_{product_id}"
#     }

#     order = client.order.create(data=data)  

#     # Save order details in the database
#     latest_payment = PaymentAccept.objects.create(
#         Product_name=product_name,
#         amount=product_amount,
#         order_id=order["id"],
#         status=order["status"]
#     )





#     return render(request, 'PaymentPage.html', {'latest_payment': latest_payment})



@login_required
def PaymentCreated(request, product_ids):
    """Create Razorpay order and save details in the database"""
    product_ids = product_ids.split(',')  # Split the product_ids string into a list of product IDs
    products = Product.objects.filter(id__in=product_ids)  # Get products from the database

    # Calculate total amount
    total_amount = sum([product.price for product in products])  # Sum the prices of the selected products

    # Razorpay order data
    data = {
        "amount": int(total_amount) * 100,  # Convert to paise (as Razorpay accepts amount in paise)
        "currency": "INR",
        "receipt": f"order_rcptid_{'_'.join(product_ids)}"
    }

    order = client.order.create(data=data)  # Create Razorpay order

    # Save order details in the database
    latest_payment = PaymentModel.objects.create(
        Product_name=', '.join([product.name for product in products]),
        amount=total_amount,
        order_id=order["id"],
        status=order["status"]
    )

    return render(request, 'PaymentPage.html', {'latest_payment': latest_payment, 'products': products})

# Payment verification function
def verify_payment(request):
    """Verify Razorpay payment and update order status"""
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        payment_id = request.POST.get("payment_id")
        signature = request.POST.get("signature")

        payment = get_object_or_404(PaymentModel, order_id=order_id)

        try:
            # Verify payment signature
            client.utility.verify_payment_signature({
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature
            })
            
            # Update payment status
            payment.payment_id = payment_id
            payment.status = "Paid"
            payment.save()


            # return into address page 

            return JsonResponse({"status": "success", "message": "Payment verified successfully", "redirect_url": "/addresspage/"})
        
        except razorpay.errors.SignatureVerificationError:
            payment.status = "Failed"
            payment.save()
            return JsonResponse({"status": "error", "message": "Payment verification failed"})

    return JsonResponse({"status": "error", "message": "Invalid request"})


# address page 


def addresspage(request):
    return render(request,'addressPage.html')




# order done

def OrderDonePage(request):
    return render(request,'OrderDonePage.html')