import json

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.http import JsonResponse
from pathlib import Path
from django.conf import settings
from dashboard.services.field_group_service import(
    load_field_group_config
)

from dashboard.services.citation_service import(
    load_citation_config
)

from dashboard.models.raw import(
    PublicationRaw
)
from dashboard.models.fact import(
    FactPublication
)

from dashboard.services.field_group_service import(
    compute_field_group
)

from dashboard.services.citation_service import (
    compute_citation_group
)

from dashboard.services.config_service import(
    set_dirty,
    is_dirty,
    clear_dirty
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
    
    setting_citation_groups = load_citation_config()

    citations = list(

        FactPublication.objects.values_list(

            "cited_by",

            flat=True

        )

    )
    bins = [(0, 0),(1, 5),(6, 10),(11, 20),(21, 50),(51, 100),(101, 200),(201, 500),(501, None)]
    histogram_labels = []

    histogram_values = []

    for min_value, max_value in bins:

        if max_value is None:

            label = f"{min_value}+"

            count = sum(

                x >= min_value

                for x in citations

            )

        else:

            label = f"{min_value}-{max_value}"

            count = sum(

                min_value <= x <= max_value

                for x in citations

            )

        histogram_labels.append(label)

        histogram_values.append(count)
    
    context = {
        "groups": groups,
        "setting_citation_groups": setting_citation_groups,
        "histogram_labels": histogram_labels,
        "histogram_values":histogram_values,
        "config_dirty": is_dirty()
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
        
        set_dirty()

        return JsonResponse({

            "success":

                True

        })


@require_POST

def save_citation_groups(request):


    try:

        payload = json.loads(

            request.body

        )

        groups = payload.get(

            "groups",

            []

        )

        # ==================================
        # VALIDATE EMPTY
        # ==================================

        if not groups:

            return JsonResponse({

                "success": False,

                "message":
                    "Danh sách nhóm trích dẫn rỗng"

            })

        # ==================================
        # SORT
        # ==================================

        groups = sorted(

            groups,

            key=lambda x: x["min"]

        )

        # ==================================
        # VALIDATE
        # ==================================

        for i, group in enumerate(groups):

            min_value = group["min"]

            max_value = group["max"]
            if i==0:
                if min_value!=0:
                    return JsonResponse({

                        "success": False,

                        "message":

                            f"Phải có một khoảng có giá trị bắt đầu = 0"
                    })
            if i==len(groups)-1:
                print(max_value)
                if max_value is not None:
                    return JsonResponse({

                        "success": False,

                        "message":

                            f"Phải có một nhóm cuối có giá trị từ N cho đến vô cùng"
                    })

            if max_value is not None:

                if min_value > max_value:

                    return JsonResponse({

                        "success": False,

                        "message":

                            f"Khoảng {min_value}-{max_value} không hợp lệ"

                    })

            if i > 0:

                previous = groups[i - 1]

                previous_max = previous["max"]

                if previous_max is None:

                    return JsonResponse({

                        "success": False,

                        "message":

                            "Chỉ được phép có một khoảng vô cực"

                    })

                if min_value != previous_max + 1:

                    return JsonResponse({

                        "success": False,

                        "message":

                            "Các khoảng phải liên tục và không có chồng chéo nhau về khoảng giá trị"

                    })

        # ==================================
        # BUILD JSON
        # ==================================

        result = []

        for group in groups:

            min_value = group["min"]

            max_value = group["max"]

            # ------------------------------
            # 0 citation
            # ------------------------------

            if (

                min_value == 0

                and

                max_value == 0

            ):

                code = "0"

                label = (

                    "Chưa được trích dẫn"

                )

            # ------------------------------
            # infinity
            # ------------------------------

            elif max_value is None:

                code = f"{min_value}+"

                label = (

                    f"Trên {min_value - 1} trích dẫn"

                )

            # ------------------------------
            # normal
            # ------------------------------

            else:

                code = (

                    f"{min_value}-{max_value}"

                )

                label = (

                    f"{min_value}–{max_value} trích dẫn"

                )

            result.append({

                "code": code,

                "label": label,

                "min": min_value,

                "max": max_value

            })

        # ==================================
        # SAVE FILE
        # ==================================
        CONFIG_PATH = (
            Path(settings.BASE_DIR)
            / "config"
            / "citation_groups.json"
        )

        with open(

            CONFIG_PATH,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                result,

                f,

                indent=4,

                ensure_ascii=False

            )

        # ==================================
        # DIRTY FLAG
        # ==================================

        set_dirty()

        return JsonResponse({

            "success": True,
            "message": "Lưu thay đổi phân nhóm trích dẫn thành công"

        })

    except Exception as e:

        return JsonResponse({

            "success": False,

            "message": str(e)

        })

    

def rebuild_fact_publication():

    publications = FactPublication.objects.only("id", "field", "subfield", "cited_by", "field_group", "citation_group")

    updated_objects = []

    for publication in publications:

        new_field_group = (

            compute_field_group(

                publication.field,

                publication.subfield

            )

        )

        new_citation_group = (

            compute_citation_group(

                publication.cited_by

            )

        )

        if (

            publication.field_group
            != new_field_group

            or

            publication.citation_group
            != new_citation_group

        ):

            publication.field_group = (

                new_field_group

            )

            publication.citation_group = (

                new_citation_group

            )

            updated_objects.append(

                publication

            )

    if updated_objects:

        FactPublication.objects.bulk_update(

            updated_objects,

            [

                "field_group",

                "citation_group"

            ],

            batch_size=1000

        )

    return {

        "total":
            len(publications),

        "updated":
            len(updated_objects)

    }
    

@require_POST

def apply_config(request):

    result = rebuild_fact_publication()

    clear_dirty()

    return JsonResponse({

        "success": True,
        "updated": result["updated"],
        "total": result["total"]

    })