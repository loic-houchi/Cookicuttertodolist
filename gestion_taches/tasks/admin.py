from django.contrib import admin
from gestion_taches.tasks.models import Task, Category

# Configuration de l'interface admin pour le modèle Task
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'due_date', 'priority', 'is_completed', 'created_at')
    list_filter = ('priority', 'is_completed', 'due_date', 'category')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)

# Configuration de l'interface admin pour le modèle Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('user',)
    search_fields = ('name',)