import datetime
from django.utils import timezone


def unix_to_datetime(timestamp):
    """Convert Unix timestamp to timezone-aware datetime."""
    naive_datetime = datetime.datetime.fromtimestamp(timestamp)
    return timezone.make_aware(naive_datetime, timezone.get_current_timezone())

