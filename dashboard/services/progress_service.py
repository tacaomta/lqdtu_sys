from django.utils import timezone


def update_import_progress(

    batch,

    step,

    current=0,

    total=0,

    percent=0

):

    batch.current_step = step

    batch.progress_current = current

    batch.progress_total = total

    batch.progress_percent = percent


    batch.save(
        update_fields=[

            "current_step",

            "progress_current",

            "progress_total",

            "progress_percent"

        ]
    )