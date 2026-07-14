from datetime import time


def _normalize_time(value: time) -> time:
    return value.replace(tzinfo=None) if value.tzinfo is not None else value


def is_within_business_hours(
    start_time: time,
    end_time: time,
    opening_time: time,
    closing_time: time,
) -> bool:
    start_time = _normalize_time(start_time)
    end_time = _normalize_time(end_time)
    opening_time = _normalize_time(opening_time)
    closing_time = _normalize_time(closing_time)

    return (
        start_time >= opening_time
        and end_time <= closing_time
    )