from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("core/", include("snack.core.urls")),
    path("order/", include("snack.order.urls")),
]
