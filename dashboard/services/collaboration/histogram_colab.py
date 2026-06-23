from django.db.models import Count

def build_histogram_data(queryset, field_name):

    rows = (
        queryset
        .values(field_name)
        .annotate(total=Count("id"))
        .order_by(field_name)
    )

    labels = [
        str(row[field_name])
        for row in rows
    ]

    values = [
        row["total"]
        for row in rows
    ]

    return labels, values