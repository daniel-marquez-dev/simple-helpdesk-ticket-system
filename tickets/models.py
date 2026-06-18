from django.db import models
from django.conf import settings  # 1. Importas settings
from django.contrib.auth.models import User



class Ticket(models.Model):
   STATUS_CHOICES = [
       ("new", "New"),
       ("in_progress", "In Progress"),
       ("resolved", "Resolved"),
       ("closed", "Closed"),
   ]

   PRIORITY_CHOICES = [
       ("low", "Low"),
       ("medium", "Medium"),
       ("high", "High"),
       ("critical", "Critical"),
   ]

   CATEGORY_CHOICES = [
       ("hardware", "Hardware"),
       ("software", "Software"),
       ("network", "Network"),
       ("access", "Access"),
       ("other", "Other"),
   ]

   title = models.CharField(max_length=200)
   description = models.TextField()
   category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
   priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
   status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
   created_by = models.ForeignKey(User, on_delete=models.CASCADE)
   created_at = models.DateTimeField(auto_now_add=True)

# ... Aquí ya debería estar el modelo Ticket del Intern 1 ...

class Comment(models.Model):
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']  # Los comentarios antiguos aparecen primero

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"Comentario de {self.author.username} en {self.ticket.title}"
