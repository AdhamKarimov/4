from django.urls import path
from .views import ProductListCreateView ,ProductUpdateDetailDeleteView


urlpatterns = [
    path('list/', ProductListCreateView.as_view(), name='list'),
    path('detail/<int:pk>/',ProductUpdateDetailDeleteView.as_view(), name='detail'),
]