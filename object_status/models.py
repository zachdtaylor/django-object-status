from django.db import models


IN_PROGRESS = 'in_progress'
NEEDS_REVIEW = 'needs_review'
IN_PRODUCTION = 'in_production'


class StatusBase(models.Model):
  STATUS_CHOICES = [
    (IN_PROGRESS, 'In Progress'),
    (NEEDS_REVIEW, 'Ready for Review'),
    (IN_PRODUCTION, 'In Production')
  ]

  status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=IN_PROGRESS)

  class Meta:
    abstract = True