from django.urls import path, include
from django.contrib import admin  # Ajouté pour l'interface admin
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.authtoken import views as authtoken_views  # Pour token

# Configuration des URLs principales du projet
urlpatterns = [
    path('api/', include('gestion_taches.tasks.urls', namespace='tasks')),  # Inclut les URLs de l'app tasks
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('admin/', admin.site.urls),  # Admin Django
    path('accounts/', include('allauth.urls')),  # Allauth pour login/signup
    
    path('api-auth/', include('rest_framework.urls')),  # Pour session DRF
    path('api-token-auth/', authtoken_views.obtain_auth_token, name='api_token_auth'),
]