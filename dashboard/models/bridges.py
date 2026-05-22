from django.db import models

from dashboard.models.fact import (
    FactPublication
)

from dashboard.models.dimensions import (
    Author
)

# =========================================================
# PUBLICATION - AUTHOR
# =========================================================

class PublicationAuthor(models.Model):

    publication = models.ForeignKey(

        FactPublication,

        on_delete=models.CASCADE,

        related_name="publication_authors"

    )

    author = models.ForeignKey(

        Author,

        on_delete=models.CASCADE,

        related_name="publication_authors"

    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        db_table = (
            "bridge_publication_author"
        )

        unique_together = (

            "publication",

            "author"

        )

    def __str__(self):

        return (

            f"{self.publication_id} - "

            f"{self.author.name}"

        )