from datetime import date, time


ALLOWED_SECONDS = {15, 30, 45, 60}

SLOT_STARTS = {
    "Breakfast": time(5, 0),
    "Midday": time(10, 0),
    "Drive": time(15, 0),
    "Night": time(19, 0),
}

RATE_CARD = {
    "Breakfast": 1200,
    "Midday": 600,
    "Drive": 1000,
    "Night": 400,
}


def parse_day(text: str) -> date:
    value = text.strip()

    try:
        return date.fromisoformat(value)
    except ValueError:
        raise ValueError(
            f"date must be a real date like 2026-11-05, not '{value}'"
        ) from None


def parse_time(text: str) -> time:
    value = text.strip()

    try:
        aired = time.fromisoformat(value)
    except ValueError:
        raise ValueError(
            f"time must be HH:MM like 06:15, not '{value}'"
        ) from None

    if aired < time(5, 0):
        raise ValueError(f"the station is off air at {value}")

    return aired


def parse_seconds(text: str) -> int:
    value = text.strip()

    try:
        seconds = int(value)
    except ValueError:
        raise ValueError(
            f"seconds must be a whole number, not '{value}'"
        ) from None

    if seconds not in ALLOWED_SECONDS:
        raise ValueError(
            f"seconds must be 15, 30, 45 or 60, not {seconds}"
        )

    return seconds


def slot_for(aired: time) -> str:
    if aired >= SLOT_STARTS["Night"]:
        return "Night"

    if aired >= SLOT_STARTS["Drive"]:
        return "Drive"

    if aired >= SLOT_STARTS["Midday"]:
        return "Midday"

    return "Breakfast"


def spot_price(slot: str, seconds: int) -> int:
    return RATE_CARD[slot] * seconds // 30


def parse_row(row: dict[str, str]) -> dict:
    spot_id = row["spot_id"].strip()
    day = parse_day(row["date"])
    aired = parse_time(row["time"])

    advertiser = row["advertiser"].strip()

    if not advertiser:
        raise ValueError("advertiser is blank")

    seconds = parse_seconds(row["seconds"])

    slot = slot_for(aired)
    amount = spot_price(slot, seconds)

    return {
        "spot_id": spot_id,
        "date": day,
        "advertiser": advertiser,
        "seconds": seconds,
        "slot": slot,
        "amount": amount,
    }


def check_rows(
    rows: list[dict[str, str]],
) -> tuple[list[dict], list[str]]:
    good_spots = []
    problems = []
    seen_ids = {}

    for line, row in enumerate(rows, start=2):
        try:
            spot = parse_row(row)
        except ValueError as error:
            problems.append(f"line {line}: {error}")
            continue

        spot_id = spot["spot_id"]

        if spot_id in seen_ids:
            problems.append(
                f"line {line}: spot_id {spot_id} "
                f"is already on line {seen_ids[spot_id]}"
            )
            continue

        seen_ids[spot_id] = line
        good_spots.append(spot)

    return good_spots, problems