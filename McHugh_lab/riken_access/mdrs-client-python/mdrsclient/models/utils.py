import datetime


def iso8601_to_user_friendly(text: str) -> str:
    return datetime.datetime.fromisoformat(text).strftime("%Y/%m/%d %H:%M:%S")
