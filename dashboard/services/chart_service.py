from django.db.models import Count


# ==========================================
# BUILD SIMPLE CHART DATASET
# ==========================================

def build_chart_dataset(

    qs,

    group_field,

    value_field="id",

    agg="count",

    order_by="-total",

    custom_order = None

):

    # ======================================
    # AGGREGATION
    # ======================================

    if agg == "count":

        data = (

            qs.values(group_field)

            .annotate(
                total=Count(value_field)
            )

            .order_by(order_by)

        )

    else:

        raise ValueError(
            "Unsupported aggregation"
        )

    data_dict = {
        item['field_group'] : item['total']
        for item in data
    }

    if custom_order:
        labels = [label for label in custom_order if label in data_dict]
    else:
        labels = sorted(data_dict.keys())

    # ======================================
    # VALUES
    # ======================================

    values = [

        data_dict[label]
        for label in labels

    ]

    return {

        "labels": labels,

        "values": values

    }


# ==========================================
# BUILD STACKED CHART DATASET
# ==========================================

def build_stacked_chart_dataset(

    qs,

    x_field,

    stack_field,

    x_order=None,

    stack_order=None

):

    # ======================================
    # QUERY
    # ======================================

    raw_data = (

        qs.values(
            x_field,
            stack_field
        )

        .annotate(
            total=Count("id")
        )

    )

    # ======================================
    # CONVERT TO LOOKUP
    # ======================================

    lookup = {}

    for item in raw_data:

        x_value = item[x_field]

        stack_value = item[stack_field]

        total = item["total"]

        lookup[(x_value, stack_value)] = total

    # ======================================
    # X LABELS
    # ======================================

    if x_order:

        x_labels = [

            label

            for label in x_order

            if any(

                item[x_field] == label

                for item in raw_data

            )

        ]

    else:

        x_labels = sorted(list(set(

            item[x_field]

            for item in raw_data

        )))

    # ======================================
    # STACK LABELS
    # ======================================

    if stack_order:

        stack_labels = [

            label

            for label in stack_order

            if any(

                item[stack_field] == label

                for item in raw_data

            )

        ]

    else:

        stack_labels = sorted(list(set(

            item[stack_field]

            for item in raw_data

        )))

    # ======================================
    # DATASETS
    # ======================================

    datasets = []

    for stack_label in stack_labels:

        data = []

        for x_label in x_labels:

            total = lookup.get(

                (x_label, stack_label),

                0

            )

            data.append(total)

        datasets.append({

            "label": stack_label,

            "data": data

        })

    return {

        "labels": x_labels,

        "datasets": datasets

    }