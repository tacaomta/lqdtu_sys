import json

from django.utils import timezone

import pandas as pd

from dashboard.models.import_batch import ImportBatch

from dashboard.models.raw import (
    PublicationRaw
)

from dashboard.services.cleaners import (
    preprocess_dataframe
)

from dashboard.services.import_result import (
    ImportResult
)

from dashboard.services.openalex import (
    enrich_with_openalex,
    fetch_openalex_metadata
)

from dashboard.services.json_service import (
    sanitize_json
)
from dashboard.services.config_service import (
    get_required_columns
)

from dashboard.services.progress_service import(
    update_import_progress
)

import os

# =========================================================
# IMPORT PUBLICATIONS
# =========================================================

def import_publications(batch_id):

    try:
        batch = ImportBatch.objects.get(

            id = batch_id

        )

        batch.status = "PROCESSING"

        batch.started_at = timezone.now()        

        file_path = batch.uploaded_file.path 

        file_size_bytes = os.path.getsize(file_path)

        file_size_kb = round( file_size_bytes / 1024, 2)

        filename = batch.filename.lower()

        batch.original_filename = file_path

        batch.file_size = file_size_kb

        batch.save()


        result = ImportResult()

        # =====================================================
        # STEP 1 — READ FILE
        # =====================================================

        result.log(
            "BƯỚC 1 — Đọc file excel/csv chứa thông tin CBKH từ nguồn Scopus"
        )


        # CSV
        if filename.endswith(".csv"):

            df = pd.read_csv(file_path)

        # EXCEL
        elif filename.endswith((".xlsx", ".xls")):

            df = pd.read_excel(file_path)

        else:

            raise ValueError(
                "Hệ thống không hỗ trợ đọc file này"
            )

        result.total_rows = len(df)

        result.log(
            f"{len(df)} bản ghi được đọc thành công"
        )

        
        update_import_progress(

            batch=batch,

            step="Đọc dữ liệu từ file",

            current=1,

            total=1,

            percent=20

        )

        batch.refresh_from_db()


        # =====================================================
        # STEP 2 — PREPROCESS
        # =====================================================

        result.log(
            "BƯỚC 2 — Tiền xử lý dữ liệu được đọc vào..."
        )

        df, duplicate_count, missing_doi_count = preprocess_dataframe(df)

        result.valid_rows = len(df)

        result.duplicates = duplicate_count

        result.log(
            f"{len(df)} bản ghi hợp lệ"
        )

        result.log(
            f"{duplicate_count} bản ghi trùng lặp được xóa"
        )

        # =====================================================
        # MISSING DOI
        # =====================================================

        result.missing_doi = missing_doi_count

        result.log(
            f"{missing_doi_count} bản ghi thiếu thông tin DOI"
        )

        
        update_import_progress(

            batch=batch,

            step="Xử lý và chuẩn hóa dữ liệu",

            current=1,

            total=1,

            percent=30

        )

        batch.refresh_from_db()

        # =====================================================
        # PREVIEW
        # =====================================================

        result.log(
            "Tạo bản xem trước..."
        )

        # ==============================================
        # REQUIRED COLUMNS
        # ==============================================

        required_columns = (
            get_required_columns()
        )

        # ==============================================
        # EXTRA COLUMNS
        # ==============================================

        extra_columns = [

            "field",

            "subfield"

        ]

        # ==============================================
        # FINAL PREVIEW COLUMNS
        # ==============================================

        preview_cols = (

            required_columns +

            extra_columns

        )

        # ==============================================
        # KEEP EXISTING ONLY
        # ==============================================

        preview_cols = [

            c
            for c in preview_cols
            if c in df.columns

        ]

        # ==============================================
        # BUILD PREVIEW DATAFRAME
        # ==============================================

        preview_df = (
            df[preview_cols]
            .copy()
        )

        # ==============================================
        # NORMALIZE COLUMN NAMES
        # ==============================================

        preview_df.columns = [

            col.lower()

            .replace(" ", "_")

            .replace("-", "_")

            for col in preview_df.columns

        ]

        result.preview_columns = list(
            preview_df.columns
        )


        # ==============================================
        # HEAD
        # ==============================================

        result.preview_head = (

            preview_df
            .head(5)
            .fillna("")
            .to_dict("records")

        )

        # ==============================================
        # TAIL
        # ==============================================

        result.preview_tail = (

            preview_df
            .tail(5)
            .fillna("")
            .to_dict("records")

        )

        result.log(
            "Đã hoàn thành bản xem trước"
        )

    # =====================================================
    # STEP 3 — CHECK DOI + ENRICH NEW DATA
    # =====================================================

        result.log(
            "BƯỚC 3 — Kiểm tra DOI và thu thập thông tin ngành, chuyên ngành..."
        )

        inserted_count = 0

        skipped_count = 0

        updated_count = 0

        existing_doi_count = 0

        new_doi_count = 0

        raw_objects = []

        now = timezone.now()

        rows_to_enrich = int(df['DOI'].notna().sum())

        current_enrich = 0

        enriched_success = 0

        enriched_failed = 0

        for idx, row in df.iterrows():

            doi = row.get("DOI")

            existing = None

            # =================================================
            # SKIP EMPTY DOI
            # =================================================

            if not doi or str(doi).strip() =="" or pd.isna(doi):

                skipped_count += 1

                continue

            # =================================================
            # CHECK EXISTING DOI
            # =================================================

            existing = (
                PublicationRaw.objects
                .filter(doi=doi)
                .first()
            )

            # =================================================
            # UPDATE EXISTING RECORD
            # =================================================

            if existing:

                existing_doi_count += 1

                new_citation = (
                    row.get("Cited by") or 0
                )

                # =============================================
                # UPDATE ONLY IF CHANGED
                # =============================================

                if existing.cited_by != new_citation:

                    existing.cited_by = new_citation

                    # =========================================
                    # MARK FOR RE-TRANSFORM
                    # =========================================

                    existing.processed = False

                    existing.processed_at = None

                    existing.save()

                    updated_count += 1

                # =============================================
                # USE EXISTING ENRICHMENT
                # =============================================

                df.at[idx, "field"] = (
                    existing.field
                )

                df.at[idx, "subfield"] = (
                    existing.subfield
                )            

                continue

            # =================================================
            # ENRICH NEW DOI ONLY
            # =================================================

            new_doi_count += 1

            metadata = fetch_openalex_metadata(doi)
            field = metadata.get("field") 
            subfield = metadata.get("subfield") 
            openalex_id = metadata.get("openalex_id")

            if field or subfield:
                enriched_success += 1
            else:
                enriched_failed += 1

            current_enrich += 1

            enrich_percent = 30 + int(

                (current_enrich / rows_to_enrich) * 60

            )

            update_import_progress(

                batch=batch,

                step="Lấy thông tin ngành, chuyên ngành",

                current=current_enrich,

                total=rows_to_enrich,

                percent=enrich_percent

            )

            batch.refresh_from_db()


            # =================================================
            # UPDATE DATAFRAME FOR PREVIEW
            # =================================================

            df.at[idx, "field"] = field

            df.at[idx, "subfield"] = subfield

            df.at[idx, "openalex_id"] = (
                openalex_id
            )

            # =================================================
            # CREATE RAW OBJECT
            # =================================================

            raw_objects.append(

                PublicationRaw(

                    title=row.get("Title"),

                    year=row.get("Year"),

                    source_title=row.get(
                        "Source title"
                    ),

                    cited_by=row.get(
                        "Cited by"
                    ) or 0,

                    doi=doi,

                    eid = row.get("EID"),

                    authors = row.get("Author full names"),

                    author_affiliations=row.get(
                        "Authors with affiliations"
                    ),

                    correspondence_address=row.get(
                        "Correspondence Address"
                    ),

                    document_type=row.get(
                        "Document Type"
                    ),

                    field=field,

                    subfield=subfield,

                    import_batch=batch,

                    source_file=filename,

                    openalex_id=openalex_id,

                    openalex_updated_at=(
                        now if openalex_id else None
                    ),

                    raw_json=sanitize_json(
                        row.to_dict()
                    )

                )

            )

    # =====================================================
    # STEP 4 — BULK INSERT
    # =====================================================

        result.log(
            "BƯỚC 4 — Lưu dữ liệu vào hệ thống..."
        )

        PublicationRaw.objects.bulk_create(

            raw_objects,

            batch_size=500

        )

        result.inserted = len(raw_objects)

        result.updated = updated_count

        update_import_progress(

            batch=batch,

            step="Lưu dữ liệu vào hệ thống",

            current=1,

            total=1,

            percent=100

        )

        batch.refresh_from_db()

        batch.status = "COMPLETED"

        batch.finished_at = timezone.now()

        batch.current_step = "Completed"

        batch.progress_percent = 100

        batch.progress_current = 100

        batch.progress_total = 100

        batch.total_rows = result.total_rows

        batch.inserted_count = result.inserted

        batch.updated_count = result.updated

        batch.duplicated_count = duplicate_count

        batch.doi_missing_count = result.missing_doi

        batch.enriched_success = enriched_success

        batch.enriched_failed = enriched_failed

        batch.existing_doi_count = existing_doi_count

        batch.new_doi_count = new_doi_count

        batch.save()


        return {

            "batch": batch,

            "result": result

        }
    
    except Exception as e:
        import traceback 
        
        print(traceback.format_exc()) 
        batch.status = "FAILED" 
        batch.error_log = str(e) 
        batch.error_message = traceback.format_exc()
        batch.save()
