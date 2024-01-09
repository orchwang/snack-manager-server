from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('snack.core.urls')),
    path('', include('snack.order.urls')),
]
