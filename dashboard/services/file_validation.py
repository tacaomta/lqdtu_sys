from dashboard.services.config_service import get_required_columns
import pandas as pd

def file_validate(file, extension):
    required_columns = set(get_required_columns())

    try:

        if extension == ".csv":

            df = pd.read_csv(
                file,
                nrows=5
            )

        else:

            df = pd.read_excel(
                file,
                nrows=5
            )
        
        columns = {str(col).strip() for col in df.columns}        
        if len(df.columns) == 0:
            return False, "File không chứa dữ liệu", required_columns
        
        if df.empty:
            return False, "File không có bản ghi", required_columns

        missing_columns = (required_columns - columns)
        if missing_columns:
            return False, "Thiếu các cột bắt buộc: " + ", ".join(sorted(missing_columns)), required_columns
        
        return True, "File hợp lệ", required_columns

    except Exception:
        return False, "Không thể đọc file", required_columns
    finally:
        file.seek(0)