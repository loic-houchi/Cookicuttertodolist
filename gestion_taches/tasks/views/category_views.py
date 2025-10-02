from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from gestion_taches.tasks.models import Category
from gestion_taches.tasks.serializers import CategorySerializer
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
import json

# ViewSet pour gérer les opérations CRUD sur les catégories via l'API
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retourne uniquement les catégories de l'utilisateur connecté
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Associe la catégorie à l'utilisateur connecté
        serializer.save(user=self.request.user)

# Vue pour gérer le dashboard des catégories (list + CRUD via POST)
def category_dashboard(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            name = request.POST.get('name')
            description = request.POST.get('description', '')
            if not name:
                return JsonResponse({'success': False, 'errors': {'name': ['Ce champ est requis.']}}, status=400)
            category = Category.objects.create(user=request.user, name=name, description=description)
            return JsonResponse({'success': True, 'message': 'Catégorie créée avec succès'})
        elif action == 'edit':
            category_id = request.POST.get('category_id')
            name = request.POST.get('name')
            description = request.POST.get('description', '')
            if not category_id or not name:
                return JsonResponse({'success': False, 'message': 'Données invalides'}, status=400)
            category = get_object_or_404(Category, id=category_id, user=request.user)
            category.name = name
            category.description = description
            category.save()
            return JsonResponse({'success': True, 'message': 'Catégorie modifiée avec succès'})
        elif action == 'delete':
            category_id = request.POST.get('category_id')
            if not category_id:
                return JsonResponse({'success': False, 'message': 'ID invalide'}, status=400)
            category = get_object_or_404(Category, id=category_id, user=request.user)
            category.delete()
            return JsonResponse({'success': True, 'message': 'Catégorie supprimée avec succès'})
        return JsonResponse({'success': False, 'message': 'Action invalide'}, status=400)
    
    # GET: Liste des catégories
    categories = Category.objects.filter(user=request.user).order_by('-id')
    categories_data = []
    for category in categories.values('id', 'name', 'description', 'created_at'):
        category_dict = dict(category)
        # Convertir la datetime en string pour la sérialisation JSON
        if category_dict['created_at']:
            category_dict['created_at'] = category_dict['created_at'].isoformat()
        categories_data.append(category_dict)
    categories_json = json.dumps(categories_data)
    return render(request, 'dashboard/pages/task/task_category.html', {
        'categories': categories,
        'categories_json': categories_json,
    })