from django.db import models


class AuthorLinkRequest(models.Model):

    STATUS_CHOICES = [

        ("PENDING", "Pending"),

        ("APPROVED", "Approved"),

        ("REJECTED", "Rejected")

    ]

    user = models.ForeignKey(

        "users.User",

        on_delete=models.CASCADE

    )

    author = models.ForeignKey(

        "dashboard.Author",

        on_delete=models.CASCADE

    )

    status = models.CharField(

        max_length=20,

        default="PENDING"

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    reviewed_by = models.ForeignKey(

        "users.User",

        null=True,

        blank=True,

        related_name="reviewed_links",

        on_delete=models.SET_NULL

    )

    reviewed_at = models.DateTimeField(

        null=True,

        blank=True

    )