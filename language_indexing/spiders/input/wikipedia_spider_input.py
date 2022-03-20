from typing import List, Optional


class WikipediaSpiderInput:
    iso_codes = []
    exclude_iso_codes = []

    def __init__(
        self,
        iso_codes: Optional[List[str]],
        exclude_iso_codes: Optional[List[str]],
        page_size: Optional[int],
        offset: Optional[str],
        max_records: Optional[int],
    ) -> None:
        self.iso_codes = iso_codes
        self.exclude_iso_codes = exclude_iso_codes
        self.page_size = page_size
        self.offset = offset
        self.max_records = max_records
