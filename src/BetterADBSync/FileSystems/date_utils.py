import re
import calendar


def datetime_string_to_posix_timestamp(date_str : str) -> float:
    """
    Special replacement for datetime.datetime.strptime() as has fails with dates before 1970
    """
    # Regular expression to capture date and time parts
    pattern = r"^(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2})$"
    match = re.match(pattern, date_str)
    if not match:
        raise ValueError(f"Invalid date: {date_str} expected format: YYYY-MM-DD HH:MM")

    year, month, day, hour, minute = map(int, match.groups())

    # Build time tuple for UTC (seconds = 0, weekday/dst ignored)
    time_tuple = (year, month, day, hour, minute, 0, 0, 0, -1)

    # Convert to POSIX timestamp (supports pre-1970)
    return calendar.timegm(time_tuple)