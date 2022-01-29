class TargetedSpiderUtil:
    @staticmethod
    def load_languages(spider_input, language_data_store):
        if spider_input.iso_codes is not None:
            return TargetedSpiderUtil._load_included_languages(spider_input, language_data_store)

        return TargetedSpiderUtil._load_all_languages(spider_input, language_data_store)

    @staticmethod
    def _load_included_languages(spider_input, language_data_store):
        result = language_data_store.get_languages(spider_input.iso_codes)

        if result.has_error():
            return []

        return result.data

    @staticmethod
    def _load_all_languages(spider_input, language_data_store):
        result = language_data_store.list_languages(
            spider_input.page_size,
            spider_input.max_records,
            offset=spider_input.offset)

        if spider_input.exclude_iso_codes is not None:
            result_filter = filter(lambda language: language.id not in spider_input.exclude_iso_codes, result.data)
            return list(result_filter)

        return result.data
