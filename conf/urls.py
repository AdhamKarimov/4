from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
   openapi.Info(
      title="CRUD API",
      default_version='v1.2',
      description="Django rest",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="adhamkarimov0000gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('product.urls')),
    path('auth/', include('user.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]