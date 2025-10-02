from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Task

@shared_task
def send_reminder(task_id=None):
    now = timezone.now()
    if task_id:
        # Handle single task
        try:
            task = Task.objects.get(id=task_id, is_completed=False, is_reminded=False, due_date__lte=now)
            send_mail(
                'Rappel de tâche',
                f'Rappel : Votre tâche "{task.title}" est due ou en retard. Description : {task.description[:50]}... Date d\'échéance : {task.due_date}.',
                'votre_email_expéditeur@example.com',
                [task.user.email],
                fail_silently=False,
            )
            task.is_reminded = True
            task.save()
        except Task.DoesNotExist:
            print(f"Tâche {task_id} non trouvée ou ne nécessite pas de rappel.")
        except Exception as e:
            print(f"Erreur envoi rappel pour tâche {task_id} : {e}")
    else:
        # Batch mode (as before)
        tasks = Task.objects.filter(
            is_completed=False,
            is_reminded=False,
            due_date__lte=now
        )
        for task in tasks:
            try:
                send_mail(
                    'Rappel de tâche',
                    f'Rappel : Votre tâche "{task.title}" est due ou en retard. Description : {task.description[:50]}... Date d\'échéance : {task.due_date}.',
                    'votre_email_expéditeur@example.com',
                    [task.user.email],
                    fail_silently=False,
                )
                task.is_reminded = True
                task.save()
            except Exception as e:
                print(f"Erreur envoi rappel pour tâche {task.id} : {e}")