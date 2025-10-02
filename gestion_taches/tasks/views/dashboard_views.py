from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from gestion_taches.tasks.models import Task, Category
from datetime import datetime, timedelta

@login_required
def dashboard_home(request):
    """
    Vue principale du tableau de bord qui affiche les statistiques et un aperçu des tâches
    """
    user = request.user
    
    # Statistiques générales
    total_tasks = Task.objects.filter(user=user).count()
    completed_tasks = Task.objects.filter(user=user, is_completed=True).count()
    pending_tasks = total_tasks - completed_tasks
    total_categories = Category.objects.filter(user=user).count()
    
    # Tâches en retard (échéance dépassée et non terminées)
    overdue_tasks = Task.objects.filter(
        user=user,
        due_date__lt=datetime.now(),
        is_completed=False
    ).count()
    
    # Tâches à venir (prochaines 7 jours)
    upcoming_deadline = datetime.now() + timedelta(days=7)
    upcoming_tasks = Task.objects.filter(
        user=user,
        due_date__lte=upcoming_deadline,
        due_date__gt=datetime.now(),
        is_completed=False
    ).count()
    
    # Tâches récentes (dernières 5 tâches créées)
    recent_tasks = Task.objects.filter(user=user).order_by('-created_at')[:5]
    
    # Tâches par priorité
    high_priority_tasks = Task.objects.filter(user=user, priority='high', is_completed=False).count()
    medium_priority_tasks = Task.objects.filter(user=user, priority='medium', is_completed=False).count()
    low_priority_tasks = Task.objects.filter(user=user, priority='low', is_completed=False).count()
    
    # Tâches par catégorie
    tasks_by_category = Category.objects.filter(user=user).annotate(
        task_count=Count('task', filter=Q(task__is_completed=False))
    ).order_by('-task_count')[:5]
    
    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'total_categories': total_categories,
        'overdue_tasks': overdue_tasks,
        'upcoming_tasks': upcoming_tasks,
        'recent_tasks': recent_tasks,
        'high_priority_tasks': high_priority_tasks,
        'medium_priority_tasks': medium_priority_tasks,
        'low_priority_tasks': low_priority_tasks,
        'tasks_by_category': tasks_by_category,
    }
    
    return render(request, 'dashboard/pages/dashboard.html', context)

