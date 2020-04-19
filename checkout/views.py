from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
"""
you want your customer to be logged in 
when they actually purchase something, go to chechout and want to pay
"""
from django.contrib import messages
from .forms import MakePaymentForm, OrderForm
from .models import OrderLineItem
from django.conf import settings
from django.utils import timezone
from products.models import Product
import stripe

# Create your views here.
stripe.api_key = settings.STRIPE_SECRET


@login_required()
def checkout(request):
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        # contains name, adress etc
        payment_form = MakePaymentForm(request.POST)
        # contains credit card details

        if order_form.is_valid() and payment_form.is_valid():
            order = order_form.save(commit=False)
            # the order form is savsed as order
            order.date = timezone.now()
            # it will take the time the btn was hit
            order.save()

            cart = request.session.get('cart', {})
            # get info on what is being purchased from current session
            total = 0
            for id, quantity in cart.items():
                product = get_object_or_404(Product, pk=id)
                #gets product id from the product being purchased
                total += quantity * product.price
                order_line_item = OrderLineItem(
                    order=order,
                    product=product,
                    quantity=quantity
                )
                order_line_item.save()
            
            # the try-except will create a customer charge, using stripe's API
            try:
                customer = stripe.Charge.create(
                    amount=int(total * 100),
                    # stripe uses everything in cents, i.e total*100
                    currency="EUR",
                    description=request.user.email,
                    card=payment_form.cleaned_data['stripe_id']
                    # the stripe ID from that form was the item hidden from the user
                )
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")
            # stripe does all the security behind, but we need to inform the user is sth has gone wrong

            if customer.paid:
                messages.error(request, "You have successfully paid")
                request.session['cart'] = {}
                return redirect(reverse('products'))
            else:
                messages.error(request, "Unable to take payment")
        else:
            print(payment_form.errors)
            messages.error(request, "We were unable to take a payment with that card!")
    else:
        payment_form = MakePaymentForm()
        order_form = OrderForm()
        # returns a blank form
    return render(request, "checkout.html", {"order_form": order_form, "payment_form": payment_form, "publishable": settings.STRIPE_PUBLISHABLE})

"""
And at the bottom, we return the checkout HTML.
And within that, we include an order form, a payment form, and a publishable key for Stripe.
So all that will be available on the HTML page when the user clicks on the checkout.
"""

