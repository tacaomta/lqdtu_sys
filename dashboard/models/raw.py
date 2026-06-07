from django.db import models


class PublicationRaw(models.Model):

    # =====================================================
    # CORE RAW DATA
    # =====================================================

    title = models.TextField()

    year = models.IntegerField(
        null=True,
        blank=True
    )

    source_title = models.TextField(
        null=True,
        blank=True
    )

    doi = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True
    )

    cited_by = models.IntegerField(
        default=0
    )

    author_affiliations = models.TextField(
        null=True,
        blank=True
    )

    correspondence_address = models.TextField(
        null=True,
        blank=True
    )

    document_type = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    # =====================================================
    # OPENALEX ENRICHMENT
    # =====================================================

    field = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True
    )

    subfield = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True
    )

    eid = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )

    openalex_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    openalex_updated_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # =====================================================
    # RAW STORAGE
    # =====================================================

    raw_json = models.JSONField()

    processed = models.BooleanField( default=False )

    processed_at = models.DateTimeField( null=True, blank=True )

    # =====================================================
    # IMPORT TRACKING
    # =====================================================

    import_batch = models.ForeignKey(
        "ImportBatch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="publications"
    )

    source_file = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    # =====================================================
    # SYSTEM TIMESTAMPS
    # =====================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        indexes = [
            models.Index(fields=["doi"]),
            models.Index(fields=["year"]),
            models.Index(fields=["field"]),
            models.Index(fields=["subfield"]),
            models.Index(fields=["processed"]),
        ]

        ordering = ["-year"]

    def __str__(self):

        if self.title:
            return self.title[:100]

        return f"Publication #{self.pk}"
