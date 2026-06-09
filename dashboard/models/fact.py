from django.db import models


class FactPublication(models.Model):

    # =====================================================
    # RAW REFERENCE
    # =====================================================

    publication_raw = models.OneToOneField(

        "PublicationRaw",

        on_delete=models.CASCADE,

        related_name="fact"

    )

    # =====================================================
    # CORE DATA
    # =====================================================

    title = models.TextField()

    year = models.IntegerField()

    doi = models.CharField(

        max_length=255,

        null=True,

        blank=True

    )

    cited_by = models.IntegerField(
        default=0
    )

    document_type = models.CharField(

        max_length=100,

        null=True,

        blank=True

    )

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

    authors_list = models.TextField(
        blank=True,
        null=True
    )

    # =====================================================
    # BUSINESS CLASSIFICATION
    # =====================================================

    field_group = models.CharField(

        max_length=255,

        null=True,

        blank=True

    )

    citation_group = models.CharField(

        max_length=100,

        null=True,

        blank=True

    )

    # =====================================================
    # AUTHORSHIP
    # =====================================================

    author_count = models.IntegerField(
        default=1
    )

    is_coauthored = models.BooleanField(
        default=False
    )

    is_first_author = models.BooleanField(
        default=False
    )

    is_corresponding = models.BooleanField(
        default=False
    )

    # =====================================================
    # COLLABORATION
    # =====================================================

    is_international_collaboration = (
        models.BooleanField(
            default=False
        )
    )

    is_domestic_collaboration = (
        models.BooleanField(
            default=False
        )
    )

    # =====================================================
    # TRACKING
    # =====================================================

    transformed_at = models.DateTimeField(
        auto_now=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # =====================================================
    # META
    # =====================================================

    class Meta:

        indexes = [

            models.Index(fields=["year"]),

            models.Index(fields=["field_group"]),

            models.Index(fields=["citation_group"]),

            models.Index(fields=["document_type"]),

            models.Index(fields=["is_first_author"]),

            models.Index(fields=["is_corresponding"]),

            models.Index(fields=["is_coauthored"]),

            models.Index(
                fields=[
                    "is_international_collaboration"
                ]
            ),

            models.Index(
                fields=[
                    "is_domestic_collaboration"
                ]
            )

        ]

    # =====================================================
    # STRING
    # =====================================================

    def __str__(self):

        return (
            f"{self.title[:80]}"
        )