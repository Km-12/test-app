class StringUtil:

    # 文字列がNoneまたは空文字なのか確認する
    @staticmethod
    def is_string_none_or_empty(str):
        if str is None or str == "":
            return True
        else:
            return False
