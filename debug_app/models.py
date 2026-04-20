from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ErrorSolution(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='error_solutions'
    )
    error_title = models.CharField(max_length=200)
    error_description = models.TextField()
    solution = models.TextField()

    # FIXED: Proper relationship instead of CharField
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='errors'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.error_title

    class Meta:
        ordering = ['-created_at']