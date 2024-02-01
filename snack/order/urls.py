from django.urls import path

from snack.order.views.order_views import (
    OrderView,
    RetrieveUpdateOrderView,
    RetrieveSnackView,
    OrderStatusUpdateView,
    TestOrderListView,
)
from snack.order.views.snack_views import SnackView, SnackReactionViewSet


urlpatterns = [
    path('orders/', OrderView.as_view()),
    path('test-orders/', TestOrderListView.as_view()),
    path('orders/<str:uid>/', RetrieveUpdateOrderView.as_view()),
    path('orders/<str:uid>/status/', OrderStatusUpdateView.as_view()),
    path('snacks/', SnackView.as_view()),
    path('snacks/<str:uid>/', RetrieveSnackView.as_view()),
    path('snacks/<str:uid>/reaction/', SnackReactionViewSet.as_view({'post': 'create'})),
]
