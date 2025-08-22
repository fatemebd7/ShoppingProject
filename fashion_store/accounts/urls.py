from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import SignupViewSet, CustomTokenObtainPairView, ProfileViewSet
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
signup = SignupViewSet.as_view({"post": "signup"})

urlpatterns = [
    path("auth/signup/", signup, name="signup"),
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
    path("profile/", ProfileViewSet.as_view({"get": "list", "post": "create"})),
    path("profile/<int:pk>/", ProfileViewSet.as_view({
        "get": "retrieve", "put": "update", "patch": "partial_update"
    })),
]
