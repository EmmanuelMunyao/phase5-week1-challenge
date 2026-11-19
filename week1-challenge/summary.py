from checks import RATE_CARD


def totals_by_advertiser(
    spots: list[dict],
) -> dict[str, dict[str, int]]:
    totals = {}

    for spot in spots:
        advertiser = spot["advertiser"]

        if advertiser not in totals:
            totals[advertiser] = {
                "spots": 0,
                "seconds": 0,
                "amount": 0,
            }

        totals[advertiser]["spots"] += 1
        totals[advertiser]["seconds"] += spot["seconds"]
        totals[advertiser]["amount"] += spot["amount"]

    return totals


def totals_by_slot(spots: list[dict]) -> dict[str, int]:
    totals = {
        slot: 0
        for slot in RATE_CARD
    }

    for spot in spots:
        totals[spot["slot"]] += spot["amount"]

    return totals


def ranked(
    totals: dict[str, dict[str, int]],
) -> list[tuple[str, dict]]:
    return sorted(
        totals.items(),
        key=lambda item: (-item[1]["amount"], item[0]),
    )


def build_report(
    source: str,
    rows_read: int,
    spots: list[dict],
    rejected: list[str],
) -> dict:
    advertiser_totals = totals_by_advertiser(spots)
    slot_totals = totals_by_slot(spots)
    ranked_advertisers = ranked(advertiser_totals)

    dates = [spot["date"] for spot in spots]

    return {
        "station": "Sauti ya Nkubu FM",
        "source": source,
        "first_day": min(dates).isoformat(),
        "last_day": max(dates).isoformat(),
        "rows_read": rows_read,
        "accepted": len(spots),
        "rejected": len(rejected),
        "total_ksh": sum(spot["amount"] for spot in spots),
        "advertisers": [
            {
                "name": name,
                "spots": values["spots"],
                "seconds": values["seconds"],
                "amount_ksh": values["amount"],
            }
            for name, values in ranked_advertisers
        ],
        "slots_ksh": slot_totals,
        "problems": rejected,
    }