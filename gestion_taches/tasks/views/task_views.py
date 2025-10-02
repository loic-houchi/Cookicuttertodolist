from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from gestion_taches.tasks.models import Task, Category
from gestion_taches.tasks.serializers import TaskSerializer
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
import json
from datetime import datetime
from django.core.mail import send_mail  # Ajouté pour l'email
from django.core.serializers.json import DjangoJSONEncoder

# ViewSet pour gérer les opérations CRUD sur les tâches via l'API
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at', 'priority']

    def get_queryset(self):
        # Retourne uniquement les tâches de l'utilisateur connecté
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        task = serializer.save(user=self.request.user)
        # Pas de send_reminder.delay ici (géré par Celery Beat)
        # Envoi notification email pour création (cohérence avec dashboard)
        try:
            send_mail(
                'Tâche créée avec succès',
                f'Votre tâche "{task.title}" a été créée. Description : {task.description[:50]}... Date d\'échéance : {task.due_date if task.due_date else "Aucune"}.',
                'votre_email_expéditeur@example.com',
                [self.request.user.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Erreur envoi email : {e}")
            
    def perform_update(self, serializer):
        old_due_date = serializer.instance.due_date
        task = serializer.save()
        if old_due_date != task.due_date:
            task.is_reminded = False
            task.save()
        # Envoi notification email pour modification
        try:
            send_mail(
                'Tâche modifiée avec succès',
                f'Votre tâche "{task.title}" a été modifiée. Description : {task.description[:50]}... Date d\'échéance : {task.due_date if task.due_date else "Aucune"}.',
                'votre_email_expéditeur@example.com',
                [self.request.user.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Erreur envoi email : {e}")
            

    def perform_destroy(self, instance):
        title = instance.title
        user_email = instance.user.email
        instance.delete()
        # Envoi notification email pour suppression
        try:
            send_mail(
                'Tâche supprimée',
                f'Votre tâche "{title}" a été supprimée.',
                'votre_email_expéditeur@example.com',
                [user_email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Erreur envoi email : {e}")

# Vue pour gérer le dashboard des tâches (list + CRUD via POST)
def task_dashboard(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            title = request.POST.get('title')
            description = request.POST.get('description', '')
            due_date_str = request.POST.get('due_date', None)
            category_id = request.POST.get('category', None)
            if not title:
                return JsonResponse({'success': False, 'errors': {'title': ['Ce champ est requis.']}}, status=400)
            due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M') if due_date_str else None
            category = get_object_or_404(Category, id=category_id, user=request.user) if category_id else None
            task = Task.objects.create(
                user=request.user,
                title=title,
                description=description,
                due_date=due_date,
                category=category,
                priority='medium'  # Default, adapter si besoin
            )
            from gestion_taches.tasks.tasks import send_reminder
            if task.due_date:
                send_reminder.delay(task.id)
            
            # Ajout : Envoyer notification email pour création
            try:
                send_mail(
                    'Tâche créée avec succès',
                    f'Votre tâche "{task.title}" a été créée. Description : {task.description[:50]}... Date d\'échéance : {task.due_date if task.due_date else "Aucune"}.',
                    'votre_email_expéditeur@example.com',  # Remplacez par votre email from
                    [request.user.email],  # Email de l'utilisateur connecté
                    fail_silently=False,
                )
            except Exception as e:
                # Gérer l'erreur silencieusement ou logger
                print(f"Erreur envoi email : {e}")
            
            return JsonResponse({'success': True, 'message': 'Tâche créée avec succès'})
        
        elif action == 'edit':
            task_id = request.POST.get('task_id')
            title = request.POST.get('title')
            description = request.POST.get('description', '')
            due_date_str = request.POST.get('due_date', None)
            category_id = request.POST.get('category', None)
            if not task_id or not title:
                return JsonResponse({'success': False, 'message': 'Données invalides'}, status=400)
            due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M') if due_date_str else None
            category = get_object_or_404(Category, id=category_id, user=request.user) if category_id else None
            task = get_object_or_404(Task, id=task_id, user=request.user)
            old_due_date = task.due_date
            task.title = title
            task.description = description
            task.due_date = due_date
            task.category = category
            task.save()
            if old_due_date != task.due_date:  # Nouveau : reset is_reminded si due_date change
                task.is_reminded = False
                task.save()
            
            # Ajout : Envoyer notification email pour modification
            try:
                send_mail(
                    'Tâche modifiée avec succès',
                    f'Votre tâche "{task.title}" a été modifiée. Description : {task.description[:50]}... Date d\'échéance : {task.due_date if task.due_date else "Aucune"}.',
                    'votre_email_expéditeur@example.com',  # Remplacez par votre email from
                    [request.user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Erreur envoi email : {e}")
            
            return JsonResponse({'success': True, 'message': 'Tâche modifiée avec succès'})
        
        elif action == 'delete':
            task_id = request.POST.get('task_id')
            if not task_id:
                return JsonResponse({'success': False, 'message': 'ID invalide'}, status=400)
            task = get_object_or_404(Task, id=task_id, user=request.user)
            title = task.title  # Nouveau : sauvegarde pour email
            task.delete()
            # Nouveau : Envoyer notification email pour suppression
            try:
                send_mail(
                    'Tâche supprimée',
                    f'Votre tâche "{title}" a été supprimée.',
                    'votre_email_expéditeur@example.com',
                    [request.user.email],
                    fail_silently=False,
                    )
            except Exception as e:
                print(f"Erreur envoi email : {e}")
                
            return JsonResponse({'success': True, 'message': 'Tâche supprimée avec succès'})
        
        return JsonResponse({'success': False, 'message': 'Action invalide'}, status=400)
    
    # GET: Liste des tâches
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    tasks_json = json.dumps(
        list(tasks.values('id', 'title', 'description', 'due_date', 'category__name', 'created_at')),
        cls=DjangoJSONEncoder
    )   

    categories = Category.objects.filter(user=request.user)
    return render(request, 'dashboard/pages/task/task.html', {
        'tasks': tasks,
        'tasks_json': tasks_json,
        'categories': categories,
    })