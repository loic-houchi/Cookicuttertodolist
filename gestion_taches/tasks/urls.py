from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
from gestion_taches.tasks.views.category_views import CategoryViewSet, category_dashboard
from gestion_taches.tasks.views.task_views import TaskViewSet, task_dashboard
from gestion_taches.tasks.views.dashboard_views import dashboard_home

# Nom de l'application pour le namespace
app_name = 'tasks'

# Configuration des routes pour l'API des tâches et catégories
router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', dashboard_home, name='home'),
    path('dashboard/', dashboard_home, name='dashboard'),
    path('category/', category_dashboard, name='category'),
    path('task/', task_dashboard, name='task'),
    # Routes temporaires pour éviter les erreurs
    path('company-settings/', TemplateView.as_view(template_name='dashboard/index.html'), name='company_settings_manage'),
    path('activity-log/', TemplateView.as_view(template_name='dashboard/index.html'), name='activity_log'),
]