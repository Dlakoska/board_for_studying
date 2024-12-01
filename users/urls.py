from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from users.apps import UsersConfig
from users.views import UserRetrieveAPIView, UserCreateAPIView, UserListAPIView, UserDestroyAPIView, \
    UserUpdateAPIView, PaymentViewSet
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name

router = SimpleRouter()
router.register("payments", PaymentViewSet)

urlpatterns = [
    # Пользователь
    path("users/", UserListAPIView.as_view(), name="users"),
    path("user/register/", UserCreateAPIView.as_view(), name="user_register"),
    path("user/<int:pk>/", UserRetrieveAPIView.as_view(), name="user_retrieve"),
    path("user/<int:pk>/update/", UserUpdateAPIView.as_view(), name="user_update"),
    path("user/<int:pk>/delete/", UserDestroyAPIView.as_view(), name="user_retrieve"),
    # Токены
    path("user/token/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='token_obtain_pair'),
    path("user/token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    # path("user/payments/<int:course_id>/", PaymentCreateAPIView.as_view(), name="payments_create")

]
urlpatterns += router.urls
