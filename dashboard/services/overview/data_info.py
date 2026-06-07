from django.db.models import (
    Q
)
from dashboard.models.fact import (
    FactPublication
)
from dashboard.models.import_batch import(
    ImportBatch
)


def get_data_info():

    qs_no_filter = FactPublication.objects.all()
    total_publications = qs_no_filter.count()

    missing_field_count = (

        qs_no_filter.filter(

            Q(field__isnull=True)

            |

            Q(field="")

            |

            Q(subfield__isnull=True)

            |

            Q(subfield="")

        )

        .count()

    )
    missing_field_percent = (

        round(

            missing_field_count

            / total_publications

            * 100,

            1

        )

        if total_publications > 0

        else 0

    )

    field_count = FactPublication.objects.exclude(field__isnull=True).exclude(field="").values_list("field", flat=True).distinct().count()
    subfield_count = FactPublication.objects.exclude(subfield__isnull=True).exclude(subfield="").values_list("subfield", flat=True).distinct().count()
    document_type_count = FactPublication.objects.values("document_type").distinct().count()
    other_count = FactPublication.objects.filter(field_group="Others").count()
    other_percent = round(other_count / total_publications*100, 1) if total_publications>0 else 0
    year_count = FactPublication.objects.exclude(year__isnull=True).values_list("year", flat=True).distinct().count()



    data_quality = {
        "total_publications": total_publications,
        "missing_field_count":missing_field_count,
        "missing_field_percent":missing_field_percent,
        "field_count":field_count,
        "subfield_count":subfield_count,
        "document_type_count":document_type_count,
        "year_count":year_count,
        "other_count":other_count,
        "other_percent":other_percent
    }

    return data_quality


