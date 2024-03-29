from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from snack.core.views.auth_views import (
    IsAdminCheckView,
    AuthenticationCheckView,
    UserSignUpView,
    UserProfileView,
    UserListView,
    UpdateUserView,
    UserResignView,
)


urlpatterns = [
    path('checks/is_admin/', IsAdminCheckView.as_view()),
    path('checks/is_authenticated/', AuthenticationCheckView.as_view()),
]

urlpatterns += [
    path('auth/sign-up/', UserSignUpView.as_view(), name='user_sign_up'),
    path('auth/users/profile/', UserProfileView.as_view(), name='user_profile'),
    path('auth/users/', UserListView.as_view(), name='user_list'),
    path('auth/users/resign/', UserResignView.as_view(), name='user_resign'),
    path('auth/users/<str:id>/', UpdateUserView.as_view(), name='update_user'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
