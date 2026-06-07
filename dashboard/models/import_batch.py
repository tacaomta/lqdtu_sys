from django.db import models
from django.conf import settings




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


    uploaded_file = models.FileField(
        upload_to="imports/%Y/%m/",
        default="imports"
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

    # Số bản ghi lưu vào CSDL = total_rows - duplicated_count
    inserted_count = models.IntegerField(
        default=0
    )

    existing_doi_count = models.IntegerField(default=0)

    new_doi_count = models.IntegerField(default=0)

    # Đây là chỉ số khi DOI đã tồn tại trong CSDL nhưng Khác Citation thì được cập nhật lại
    updated_count = models.IntegerField(
        default=0
    )

    # Có DOI là NAN
    doi_missing_count = models.IntegerField(
        default=0
    )

    # Trùng số DOI
    duplicated_count = models.IntegerField(
        default=0
    )

    enriched_success = models.IntegerField(
        default=0
    )

    # Có DOI là không valid, hoặc không lấy được chuyên ngành
    enriched_failed = models.IntegerField(
        default=0
    )

    data_updated_until = models.DateField(
    null=True,
    blank=True)

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
        settings.AUTH_USER_MODEL,
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

    current_step = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    progress_current = models.IntegerField(
        default=0
    )

    progress_total = models.IntegerField(
        default=0
    )

    progress_percent = models.IntegerField(
        default=0
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
