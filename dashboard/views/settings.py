import json

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.http import JsonResponse
from pathlib import Path
from dashboard.services.field_group_service import(
    load_field_group_config
)
from dashboard.models.raw import(
    PublicationRaw
)

@login_required
def settings_view(request):

    field_groups_setting = load_field_group_config()
    groups = []

    for group_name, config in field_groups_setting.items():

        groups.append({

            "name":
                group_name,

            "fields":
                config.get(
                    "fields",
                    []
                ),

            "subfields":
                config.get(
                    "subfields",
                    []
                ),
            "editable":
                group_name!="Others"
        })
    
    context = {
        "groups": groups
    }

    return render(request, "dashboard/settings.html", context=context)

def field_group_detail(request, group_name):

    field_groups_setting = load_field_group_config()

    group = field_groups_setting.get(

        group_name,

        {}

    )

    all_fields = list(

        PublicationRaw.objects

        .exclude(field="")

        .values_list(

            "field",

            flat=True

        )

        .distinct()

        .order_by("field")

    )

    all_subfields = list(

        PublicationRaw.objects

        .exclude(subfield="")

        .values_list(

            "subfield",

            flat=True

        )

        .distinct()

        .order_by("subfield")

    )

    return JsonResponse({

        "group":

            group_name,

        "fields":

            group.get(

                "fields",

                []

            ),

        "subfields":

            group.get(

                "subfields",

                []

            ),

        "all_fields":

            all_fields,

        "all_subfields":

            all_subfields

    })


@require_POST
def save_field_group(request):

    payload = json.loads(

        request.body

    )

    group_name = payload["group"]
    fields = payload["fields"]
    subfields = payload["subfields"]

    if len(fields)==0:
        return JsonResponse({

            "success": False,

            "message": "Chưa chuyên ngành nào được chọn vào nhóm này",
            "duplicates": ""})

    field_groups_setting = load_field_group_config()

    field_groups_setting[group_name] = {

        "fields":

            fields,

        "subfields":

            subfields

    }
    # Tạo ra các cặp của các nhóm khác khác nhóm đang sửa
    existing_pairs = set()

    for group, config in field_groups_setting.items():

        if group == group_name:
            continue

        old_fields = config.get(
            "fields",
            []
        )

        old_subfields = config.get(
            "subfields",
            []
        )

        for field in old_fields:
            if len(old_subfields)>0:

                for subfield in old_subfields:

                    existing_pairs.add(

                        (
                            field,
                            subfield
                        )

                    )
            else:
                existing_pairs.add((field, ''))

    # Các cặp của nhóm đang sửa
    current_pairs = set()

    for field in fields:
        if len(subfields)>0:
            for subfield in subfields:

                current_pairs.add(

                    (
                        field,
                        subfield
                    )

                )
        else:
            current_pairs.add((field, ''))

    duplicated_pairs = (current_pairs & existing_pairs)
    if duplicated_pairs:

        duplicate_text = [

            f"{field} / {subfield}"

            for field, subfield

            in duplicated_pairs

        ]

        return JsonResponse({

            "success": False,

            "message":

                "Các cặp field/subfield sau đã tồn tại ở nhóm khác",

            "duplicates":

                duplicate_text

            })
    else:
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        path = (
            BASE_DIR /
            "config" /
            "field_groups.json"
        )

        with open(

            path,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                field_groups_setting,

                f,

                indent=4,

                ensure_ascii=False

            )

        return JsonResponse({

            "success":

                True

        })