from datetime import time


def is_within_business_hours(
    start_time: time,
    end_time: time,
    opening_time: time,
    closing_time: time,
) -> bool:
    return (
        start_time >= opening_time
        and end_time <= closing_time
    )