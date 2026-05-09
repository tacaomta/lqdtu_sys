import pandas as pd
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from dashboard.forms import UploadCSVForm
from dashboard.models import PublicationRaw
from dashboard.services.etl_service import transform_data


@login_required
def upload_csv(request):

    if request.method == "POST":
        form = UploadCSVForm(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES["file"]

            # đọc CSV
            df = pd.read_csv(file)

            raw_objects = []

            for _, row in df.iterrows():
                raw_objects.append(
                    PublicationRaw(
                        title=row.get("Title"),
                        year=row.get("Year"),
                        source_title=row.get("Source title"),
                        cited_by=row.get("Cited by", 0),
                        doi=row.get("DOI"),
                        authors=row.get("Authors"),
                        affiliations=row.get("Affiliations"),
                        abstract=row.get("Abstract"),
                        author_keywords=row.get("Author Keywords"),
                        index_keywords=row.get("Index Keywords"),
                        publisher=row.get("Publisher"),
                        document_type=row.get("Document Type"),
                        source=row.get("Source"),

                        raw_json=row.to_dict()
                    )
                )

            # bulk insert (nhanh hơn rất nhiều)
            PublicationRaw.objects.bulk_create(raw_objects, batch_size=500)

            # 👇 transform sang FACT + DIM
            transform_data()

            return redirect("overview")

    else:
        form = UploadCSVForm()

    return render(request, "dashboard/upload.html", {"form": form})