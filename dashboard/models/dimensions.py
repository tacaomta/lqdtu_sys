from django.db import models

# =========================================================
# COUNTRY
# =========================================================

class Country(models.Model):

    name = models.CharField(

        max_length=255,

        unique=True

    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        db_table = "dim_country"

        ordering = ["name"]

    def __str__(self):

        return self.name


# =========================================================
# UNIVERSITY
# =========================================================

class University(models.Model):

    name = models.CharField(

        max_length=500,

        unique=True

    )

    country = models.ForeignKey(

        Country,

        on_delete=models.SET_NULL,

        null=True,

        blank=True,

        related_name="universities"

    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        db_table = "dim_university"

        ordering = ["name"]

    def __str__(self):

        return self.name
    
# =========================================================
# AUTHOR
# =========================================================

class Author(models.Model):

    name = models.CharField(

        max_length=500

    )

    university = models.ForeignKey(

        University,

        on_delete=models.SET_NULL,

        null=True,

        blank=True,

        related_name="authors"

    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        db_table = "dim_author"

        unique_together = (

            "name",

            "university"

        )

        ordering = ["name"]

    def __str__(self):

        return self.name