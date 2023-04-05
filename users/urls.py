from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from . import views

urlpatterns = [
    path("users/", views.UserView.as_view()),
    path("users/<uuid:pk>/", views.UserDetailedView.as_view()),
    path("login/", jwt_views.TokenObtainPairView.as_view()),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
