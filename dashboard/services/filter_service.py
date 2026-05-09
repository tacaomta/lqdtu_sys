def get_years():
    from dashboard.models import FactPublication

    years = FactPublication.objects.values_list('year', flat=True).distinct().order_by('year')

    years = list(years)

    # 👉 fallback nếu DB trống
    if not years:
        years = list(range(2020, 2026))  # hoặc range bạn muốn

    return years


def get_fields():
    from dashboard.models import DimField  # nếu có bảng dimension

    fields = list(
        DimField.objects.values_list("name", flat=True)
    )

    # 👉 fallback nếu DB chưa có
    if not fields:
        fields = [
            "Computer Science and Information Systems",
            "Electrical and Electronic Engineering",
            "Materials Science",
            "Chemistry",
            "Engineering and Technology",
            "Others"
        ]

    return fields

def get_citation_groups():
    CITATION_GROUPS = [

    ("50+", "Trên 50 trích dẫn"),

    ("21-50", "21–50 trích dẫn"),

    ("11-20", "11–20 trích dẫn"),

    ("6-10", "6–10 trích dẫn"),

    ("1-5", "1–5 trích dẫn"),

    ("0", "Chưa được trích dẫn"),
]
    return CITATION_GROUPS