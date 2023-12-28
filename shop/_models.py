from django.db import models


class CartStatus(models.TextChoices):
    A="A", "Active"
    D="D", "Completed"
    C='C', "Cancelled"
