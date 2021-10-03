from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from authentication.views import CreateUserView, GetAllUsersView


urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/create/', CreateUserView.as_view(), name='user_create'),
    path('user/list/', GetAllUsersView.as_view(), name='user_list'),
]
