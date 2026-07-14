from datetime import datetime, date, time, timedelta


def calculate_end_time(
    start_time: time,
    duration_minutes: int,
    buffer_minutes: int = 0,
) -> time:
    start = datetime.combine(
        date.today(),
        start_time,
    )

    end = start + timedelta(
        minutes=duration_minutes + buffer_minutes
    )

    return end.time()