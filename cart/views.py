from django.shortcuts import render, redirect, reverse


# Create your views here.
def view_cart(request):
    """A View that renders the cart contents page"""
    return render(request, "cart.html")
    """ we don't have to pass in a dictionary of cart_contents because that context is available everywhere."""


def add_to_cart(request, id):
    """Add a quantity of the specified product to the cart"""
    
    quantity = int(request.POST.get('quantity'))
    """gets the int from the form we created in products.html"""

    cart = request.session.get('cart', {})
    cart[id] = cart.get(id, quantity)

    request.session['cart'] = cart
    return redirect(reverse('index'))


"""You can now add an item to the cart. 
However, if you try adding the same item to the cart again, 
you will overwrite the cart value. This behavior is not what the user wants.
 Can you think how to modify the add_to_cart view to improve the user experience?"""

"""
Hint:
If the item is already in the cart, 
you want to add the new quantity to the existing quantity. 
However, if the item is not in the cart, 
then the current add_to_cart view works. 
Try an if/else statement.
"""

def adjust_cart(request, id):
    """
    Adjust the quantity of the specified product to the specified
    amount
    """
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    """So again, we either get a cart that exists or one that is empty if one has not yet been created."""

    if quantity > 0:
        """we can only adjust if a quantity is greater than 0.
If there's nothing in the cart, you cannot adjust it."""
        cart[id] = quantity
    else:
        cart.pop(id)
        """Remove the item at the given position in the list, and return it. If no index is specified, a.pop() removes and returns the last item in the list."""
    
    request.session['cart'] = cart
    return redirect(reverse('view_cart'))