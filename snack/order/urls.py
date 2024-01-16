from django.urls import path

from snack.order.views.order_views import OrderListView, RetrieveOrderView, RetrieveSnackView
from snack.order.views.snack_views import SnackListView


urlpatterns = [
    path('orders/', OrderListView.as_view()),
    path('orders/<str:uid>/', RetrieveOrderView.as_view()),
    path('snacks/', SnackListView.as_view()),
    path('snacks/<str:uid>/', RetrieveSnackView.as_view()),
]
