from django.db import models

class Chat(models.Model):

    name = models.CharField("Full Name", max_length=150)
    email = models.EmailField(max_length=255)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Chat Submission"
        verbose_name_plural = "Chat Submissions"

    def __str__(self):
        # Good practice: Provides a human-readable name for each object.
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"