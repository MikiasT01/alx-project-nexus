from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.views.generic import RedirectView
from django.urls import path, include
from polls.views import homepage


schema_view = get_schema_view(
    openapi.Info(
        title="Online Poll System API",
        default_version='v1',
        description="API for managing polls, voting, and results",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', homepage, name='homepage'),
    path('admin/', admin.site.urls),
    path('api/', include('polls.urls')),  # App URLs
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]