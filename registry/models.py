import uuid
import random
import string
from django.db import models
import secrets

def generate_project_code():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=6))

class PublicProject(models.Model):
    registered_by = models.ForeignKey('AuthorizedInstance', on_delete=models.CASCADE, related_name='projects')
    project_code = models.CharField(max_length=10, unique=True, default=generate_project_code)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    instance_url = models.URLField(help_text="The URL of the server hosting this project")
    remote_project_id = models.CharField(max_length=100, help_text="The ID of the project on the local instance")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['registered_by', 'remote_project_id']
        
    def __str__(self):
        return f"{self.title} ({self.project_code})"
    
    


class AuthorizedInstance(models.Model):
    name = models.CharField(max_length=255, help_text="Name of the instance (e.g., Southern Highlands Server)")
    country = models.CharField(max_length=255, help_text="Country where the instance is located")
    api_key = models.CharField(max_length=128, unique=True, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.api_key:
            # Generate a secure random key prefixed for easier identification
            self.api_key = f"afyadata_{secrets.token_urlsafe(32)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.country})"
