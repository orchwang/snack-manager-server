from django.contrib import admin

from snack.order.models import Cart, Order, Snack


class CartInline(admin.TabularInline):
    model = Cart


class OrderAdmin(admin.ModelAdmin):
    inlines = [CartInline]


class SnackAdmin(admin.ModelAdmin):
    pass


admin.site.register(Order, OrderAdmin)
admin.site.register(Snack, SnackAdmin)
