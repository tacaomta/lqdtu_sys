from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name



class User(AbstractUser):
    roles = models.ManyToManyField(Role, blank=True)

    def __str__(self):
        return self.username
    
    def has_role(self, role_name):
        return self.roles.filter(name=role_name).exists()
    
    @property
    def is_author(self):

        return self.roles.filter(
            name="Author"
        ).exists()
    
    @property
    def is_manager(self):

        return self.roles.filter(
            name="MANAGER"
        ).exists()

    @property
    def is_admin(self):

        return self.roles.filter(
            name="ADMIN"
        ).exists()

class Department(models.Model):

    name = models.CharField(

        max_length=255,

        unique=True

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    def __str__(self):

        return self.name

class UserProfile(models.Model):

    user = models.OneToOneField(

        User,

        on_delete=models.CASCADE,

        related_name="profile"

    )

    author = models.ForeignKey(

        "dashboard.Author",

        null=True,

        blank=True,

        on_delete=models.SET_NULL

    )

    department = models.ForeignKey(

        Department,

        null=True,

        blank=True,

        on_delete=models.SET_NULL

    )

    fullname = models.CharField(

        max_length=255,

        blank=True

    )

    phone = models.CharField(

        max_length=30,

        blank=True

    )

    position = models.CharField(

        max_length=255,

        blank=True

    )

    degree = models.CharField(

        max_length=255,

        blank=True

    )

    orcid = models.CharField(

        max_length=50,

        blank=True

    )

    bio = models.TextField(

        blank=True

    )

    website = models.URLField(

        blank=True

    )

    must_change_password = models.BooleanField(

        default=False

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    updated_at = models.DateTimeField(

        auto_now=True

    )

class AuthorLinkRequest(models.Model):

    STATUS_CHOICES = [

        ("PENDING", "Pending"),

        ("APPROVED", "Approved"),

        ("REJECTED", "Rejected")

    ]

    user = models.ForeignKey(

        User,

        on_delete=models.CASCADE

    )

    author = models.ForeignKey(

        "dashboard.Author",

        on_delete=models.CASCADE

    )

    publication = models.ManyToManyField(
        "dashboard.FactPublication",
        blank=True,
    )

    status = models.CharField(

        max_length=20,

        default="PENDING"

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    reviewed_by = models.ForeignKey(

        User,

        null=True,

        blank=True,

        related_name="reviewed_links",

        on_delete=models.SET_NULL

    )

    reviewed_at = models.DateTimeField(

        null=True,

        blank=True

    )

