"""Select the next Metromare arrival from Astral transit records."""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

ROME = ZoneInfo("Europe/Rome")


class AstralApiError(Exception):
    """Astral could not provide usable arrival data."""


def _parse_transit(record: dict) -> tuple[datetime, int, int, int, str]:
    try:
        timestamp = datetime.fromisoformat(record["created_at"])
        hour, minute = map(int, record["orario"].split(":"))
        delay = 0 if record["ritardo"] == "" else int(record["ritardo"])
        status = record["soppressa"]
        if (
            timestamp.tzinfo is None
            or not 0 <= hour <= 23
            or not 0 <= minute <= 59
            or status not in ("S", "N")
        ):
            raise ValueError("campi del transito non validi")
    except (KeyError, AttributeError, TypeError, ValueError) as exc:
        raise AstralApiError("Risposta Astral non valida: orario del transito") from exc
    return timestamp, hour, minute, delay, status


def next_arrivals(
    records: list, now: datetime, count: int = 3
) -> tuple[datetime | None, ...]:
    """Select the next arrivals, including reported delays and missing slots."""
    if now.tzinfo is None:
        raise ValueError("now must have a timezone")
    today = now.astimezone(ROME).date()
    arrivals = []
    for record in records:
        if not isinstance(record, dict):
            raise AstralApiError("Risposta Astral non valida: transito")
        if record.get("orario") == "Invalid date":
            continue
        timestamp, hour, minute, delay, status = _parse_transit(record)
        if status == "S" or timestamp.astimezone(ROME).date() != today:
            continue
        arrival = datetime.combine(today, datetime.min.time(), ROME).replace(
            hour=hour, minute=minute
        ) + timedelta(minutes=delay)
        if arrival >= now:
            arrivals.append(arrival)
    arrivals.sort()
    return tuple((arrivals[:count] + [None] * count)[:count])
