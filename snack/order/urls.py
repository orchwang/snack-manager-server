from django.urls import path

from snack.order.views.order_views import OrderView, RetrieveOrderView, RetrieveSnackView
from snack.order.views.snack_views import SnackView


urlpatterns = [
    path('orders/', OrderView.as_view()),
    path('orders/<str:uid>/', RetrieveOrderView.as_view()),
    path('snacks/', SnackView.as_view()),
    path('snacks/<str:uid>/', RetrieveSnackView.as_view()),
]
