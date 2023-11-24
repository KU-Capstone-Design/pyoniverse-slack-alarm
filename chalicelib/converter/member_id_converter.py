from collections import UserDict


class MemberIdConverter(UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(
            {
                "윤영로": "U05PB6RK7FT",
                "김현아": "U05R2UNR0J2",
                "이승우": "U05P7C7MVRB",
                "전병국": "U05Q02RU5SL",
            }
        )
