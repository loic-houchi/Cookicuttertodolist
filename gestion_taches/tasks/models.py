

from django.db import models
from django.conf import settings

class Category(models.Model):
    """
    Modèle représentant une catégorie pour organiser les tâches.
    Une catégorie est créée par un utilisateur et peut être associée à plusieurs tâches.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories',
        help_text="Utilisateur créateur de la catégorie"
    )
    name = models.CharField(
        max_length=100,
        help_text="Nom de la catégorie (max 100 caractères)"
    )
    description = models.TextField(
        blank=True,
        help_text="Description de la catégorie (optionnel)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date de création de la catégorie"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

class Task(models.Model):
    """
    Modèle représentant une tâche dans l'application.
    Une tâche est associée à un utilisateur et peut appartenir à une catégorie.
    Elle inclut des attributs comme le titre, la description, la date d'échéance,
    la priorité et l'état (terminée ou non).
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks',
        help_text="Utilisateur assigné à la tâche"
    )
    title = models.CharField(
        max_length=200,
        help_text="Titre de la tâche (max 200 caractères)"
    )
    description = models.TextField(
        blank=True,
        help_text="Description détaillée (optionnel)"
    )
    due_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date d'échéance de la tâche (optionnel)"
    )
    is_completed = models.BooleanField(
        default=False,
        help_text="Indique si la tâche est terminée"
    )
    is_reminded = models.BooleanField(  # Nouveau champ pour les rappels
        default=False,
        help_text="Indique si un rappel email a été envoyé"
    )
    priority = models.CharField(
        max_length=20,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='medium',
        help_text="Priorité de la tâche (faible, moyenne, haute)"
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Catégorie de la tâche (optionnel)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date de création de la tâche"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date de dernière mise à jour"
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Tâche"
        verbose_name_plural = "Tâches"
        

# models.py - Définition des modèles pour l'application tasks
# Ce fichier regroupe tous les modèles de l'application de gestion des tâches.
# Il contient actuellement les modèles Task (tâche) et Category (catégorie pour organiser les tâches).
# Les modèles sont utilisés pour le CRUD via l'API, l'interface admin et les rappels automatiques via Celery.