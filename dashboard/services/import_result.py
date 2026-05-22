class ImportResult:

    def __init__(self):

        self.logs = []

        self.total_rows = 0

        self.valid_rows = 0

        self.inserted = 0

        self.existing_doi = 0

        self.new_doi = 0

        self.enriched_success = 0

        self.enriched_failed = 0

        self.saved_to_database =  0

        self.duplicates = 0

        self.errors = 0

        self.missing_doi = 0

        self.preview_head = []

        self.preview_tail = []

    # ==========================================
    # LOGGING
    # ==========================================

    def log(self, message):

        self.logs.append(message)