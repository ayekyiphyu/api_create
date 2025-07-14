from django.db import models

class PasswordReset(models.Model):
    email = models.EmailField(max_length=254)
    reset_token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Password Reset"
        verbose_name_plural = "Password Resets"

    def __str__(self):
        return f"Password Reset for {self.email}"