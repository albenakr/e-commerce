from django.shortcuts import get_object_or_404
from products.models import Product


def cart_contents(request):
    """
    Ensures that the cart contents are available when rendering
    every page
    """
    cart = request.session.get('cart', {}) 
    """So we have a cart that requests the session.So it requests the existing cart if there is one, or a blank dictionary if there's not."""

    cart_items = []
    total = 0
    product_count = 0
    
    for id, quantity in cart.items():
        """ID is the product ID and the quantity is how many the user wishes to purchase."""
        product = get_object_or_404(Product, pk=id)
        """We need our products, which we get from our product model."""
        total += quantity * product.price
        product_count += quantity
        """Our product_count just keeps on adding the quantity.
So as you add more quantity as a user, your product count goes up."""
        cart_items.append({'id': id, 'quantity': quantity, 'product': product})
    
    return {'cart_items': cart_items, 'total': total, 'product_count': product_count}
