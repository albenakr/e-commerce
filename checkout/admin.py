from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineAdminInline(admin.TabularInline):
    model = OrderLineItem
    
"""
So within the admin.py of the checkout app, we need to add those models we've just created.
Otherwise, we would be unable to edit them through the admin panel.

"""


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineAdminInline, )


admin.site.register(Order, OrderAdmin)
"""
 to register both of these with the admin site so that we can edit them if necessary.
"""
