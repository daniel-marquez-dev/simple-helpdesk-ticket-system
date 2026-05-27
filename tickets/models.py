from django.db import models

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
   #created_by = models.ForeignKey(User, on_delete=models.CASCADE)
   created_at = models.DateTimeField(auto_now_add=True)

