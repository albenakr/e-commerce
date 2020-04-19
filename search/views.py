from django.shortcuts import render
from products.models import Product

# Create your views here.
def do_search(request):
    products = Product.objects.filter(name__icontains=request.GET['q'])
    '''
    filter is a built-in function
    name__icontains=request.GET['q'] will get  whatever 'q' is returned from the form, so we'll give the form a name of 'q'.
    And whatever you type into that form will then be used to filter the products.
    '''
    return render(request, "products.html", {"products": products})