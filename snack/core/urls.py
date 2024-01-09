from django.urls import path

from snack.core.views.auth_views import IsAdminCheckView


urlpatterns = [
    path('checks/is_admin/', IsAdminCheckView.as_view()),
]
