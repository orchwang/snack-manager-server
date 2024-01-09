from django.urls import path

from snack.order.views.order_views import CartListView, RetrieveOrderView
from snack.order.views.snack_views import SnackListView


urlpatterns = [
    path('orders/', CartListView.as_view()),
    path('order/<str:uid>/', RetrieveOrderView.as_view()),
    path('snacks/', SnackListView.as_view()),
]
