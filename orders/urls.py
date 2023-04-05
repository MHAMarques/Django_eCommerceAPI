from django.urls import path
from . import views

urlpatterns = [
    path("orders/", views.OrderView.as_view()),
    path("orders/<pk>/", views.OrderDetailView.as_view()),
]
