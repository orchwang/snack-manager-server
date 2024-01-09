from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from snack.core.views.auth_views import IsAdminCheckView, UserSignUpView


urlpatterns = [
    path('checks/is_admin/', IsAdminCheckView.as_view()),
]

urlpatterns += [
    path('auth/sign-up/', UserSignUpView.as_view(), name='user_sign_up'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
