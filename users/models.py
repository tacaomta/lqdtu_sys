from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name



class User(AbstractUser):
    roles = models.ManyToManyField(Role, related_name="users")

    def __str__(self):
        return self.username
    
    def has_role(self, role_name):
        return self.roles.filter(name=role_name).exists()
