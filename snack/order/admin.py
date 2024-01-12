from django.contrib import admin

from snack.order.models import Purchase, Order, Snack


class PurchaseInline(admin.TabularInline):
    model = Purchase


class OrderAdmin(admin.ModelAdmin):
    inlines = [PurchaseInline]


class SnackAdmin(admin.ModelAdmin):
    pass


admin.site.register(Order, OrderAdmin)
admin.site.register(Snack, SnackAdmin)
