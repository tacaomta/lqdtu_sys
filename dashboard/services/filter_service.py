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