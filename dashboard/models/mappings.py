from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class ImportBatch(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("RUNNING", "Running"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    ]

    # =====================================================
    # FILE INFO
    # =====================================================

    filename = models.CharField(
        max_length=255
    )

    original_filename = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    file_size = models.BigIntegerField(
        null=True,
        blank=True
    )

    # =====================================================
    # IMPORT STATUS
    # =====================================================

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING",
        db_index=True
    )

    # =====================================================
    # IMPORT STATISTICS
    # =====================================================

    total_rows = models.IntegerField(
        default=0
    )

    inserted_count = models.IntegerField(
        default=0
    )

    updated_count = models.IntegerField(
        default=0
    )

    skipped_count = models.IntegerField(
        default=0
    )

    failed_count = models.IntegerField(
        default=0
    )

    # =====================================================
    # ERROR TRACKING
    # =====================================================

    error_message = models.TextField(
        null=True,
        blank=True
    )

    # =====================================================
    # USER TRACKING
    # =====================================================

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="import_batches"
    )

    # =====================================================
    # TIMESTAMPS
    # =====================================================

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True
    )

    finished_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # =====================================================
    # META
    # =====================================================

    class Meta:

        ordering = ["-uploaded_at"]

    # =====================================================
    # DISPLAY
    # =====================================================

    def __str__(self):

        return (
            f"{self.filename} "
            f"({self.status})"
        )
