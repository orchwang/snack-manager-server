from django.urls import path

from snack.order.views.order_views import OrderListView, PurchaseListView, RetrieveOrderView, RetrieveSnackView
from snack.order.views.snack_views import SnackListView


urlpatterns = [
    path('orders/', OrderListView.as_view()),
    path('purchases/', PurchaseListView.as_view()),
    path('order/<str:uid>/', RetrieveOrderView.as_view()),
    path('snacks/', SnackListView.as_view()),
    path('snack/<str:uid>/', RetrieveSnackView.as_view()),
]
