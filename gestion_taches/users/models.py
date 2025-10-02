from django.contrib.auth.models import AbstractUser
from django.db import models

# Modèle personnalisé pour les utilisateurs
# Étend AbstractUser pour ajouter des champs personnalisés
class User(AbstractUser):
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username