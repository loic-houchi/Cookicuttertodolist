# serializers.py - Définition des serializers pour l'application tasks
# Ce fichier regroupe les serializers utilisés pour convertir les modèles en JSON
# et valider les données entrantes pour l'API REST. Les serializers définissent
# les champs exposés, leurs validations et les champs en lecture seule.

from rest_framework import serializers
from gestion_taches.tasks.models import Task, Category

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Category.
    Convertit les instances de Category en JSON pour les requêtes API et valide les données entrantes.
    Les champs id et user sont en lecture seule pour garantir l'intégrité des données.
    """
    name = serializers.CharField(help_text="Nom de la catégorie (max 100 caractères)")

    class Meta:
        model = Category
        fields = ['id', 'user', 'name']
        read_only_fields = ['id', 'user']
# ... (rest of the file unchanged)

class TaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(help_text="Titre de la tâche (max 200 caractères)")
    description = serializers.CharField(
        help_text="Description détaillée (optionnel)", required=False
    )
    due_date = serializers.DateTimeField(
        help_text="Date d'échéance (optionnel)", required=False
    )
    is_completed = serializers.BooleanField(
        help_text="Indique si la tâche est terminée"
    )
    is_reminded = serializers.BooleanField(  # Nouveau, en lecture seule
        read_only=True,
        help_text="Indique si un rappel a été envoyé"
    )
    priority = serializers.ChoiceField(
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        help_text="Priorité de la tâche (faible, moyenne, haute)"
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        allow_null=True,
        help_text="Identifiant de la catégorie associée (optionnel)"
    )

    class Meta:
        model = Task
        fields = [
            'id', 'user', 'title', 'description', 'due_date',
            'is_completed', 'priority', 'category', 'created_at', 'updated_at', 'is_reminded'  # Ajouté is_reminded ici
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def create(self, validated_data):
        due_date = validated_data.get('due_date')
        if due_date and not timezone.is_aware(due_date):
            # Rendre aware avec le timezone actuel (ou UTC si préféré: timezone.utc)
            validated_data['due_date'] = timezone.make_aware(due_date, timezone=timezone.get_current_timezone())
        return super().create(validated_data)

    def update(self, instance, validated_data):
        due_date = validated_data.get('due_date')
        if due_date and not timezone.is_aware(due_date):
            validated_data['due_date'] = timezone.make_aware(due_date, timezone=timezone.get_current_timezone())
        return super().update(instance, validated_data)