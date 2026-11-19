from datetime import date

from summary import (
    build_report,
    ranked,
    totals_by_advertiser,
    totals_by_slot,
)


def sample_spots():
    return [
        {
            "spot_id": "NK-1",
            "date": date(2026, 11, 2),
            "advertiser": "Alpha",
            "seconds": 30,
            "slot": "Breakfast",
            "amount": 1200,
        },
        {
            "spot_id": "NK-2",
            "date": date(2026, 11, 2),
            "advertiser": "Beta",
            "seconds": 60,
            "slot": "Midday",
            "amount": 1200,
        },
        {
            "spot_id": "NK-3",
            "date": date(2026, 11, 3),
            "advertiser": "Alpha",
            "seconds": 45,
            "slot": "Drive",
            "amount": 1500,
        },
    ]


def test_totals_by_advertiser():
    totals = totals_by_advertiser(sample_spots())

    assert totals["Alpha"] == {
        "spots": 2,
        "seconds": 75,
        "amount": 2700,
    }

    assert totals["Beta"] == {
        "spots": 1,
        "seconds": 60,
        "amount": 1200,
    }


def test_totals_by_slot():
    totals = totals_by_slot(sample_spots())

    assert totals == {
        "Breakfast": 1200,
        "Midday": 1200,
        "Drive": 1500,
        "Night": 0,
    }


def test_ranked_highest_amount_first():
    totals = totals_by_advertiser(sample_spots())

    result = ranked(totals)

    assert result[0][0] == "Alpha"
    assert result[1][0] == "Beta"


def test_ranked_equal_amount_uses_name():
    totals = {
        "Zulu": {
            "spots": 1,
            "seconds": 30,
            "amount": 1000,
        },
        "Alpha": {
            "spots": 1,
            "seconds": 30,
            "amount": 1000,
        },
    }

    result = ranked(totals)

    assert [name for name, _ in result] == ["Alpha", "Zulu"]


def test_build_report():
    spots = sample_spots()
    rejected = ["line 7: bad row"]

    report = build_report(
        "adlog-2026-11.csv",
        4,
        spots,
        rejected,
    )

    assert report["station"] == "Sauti ya Nkubu FM"
    assert report["source"] == "adlog-2026-11.csv"
    assert report["first_day"] == "2026-11-02"
    assert report["last_day"] == "2026-11-03"
    assert report["rows_read"] == 4
    assert report["accepted"] == 3
    assert report["rejected"] == 1
    assert report["total_ksh"] == 3900
    assert report["slots_ksh"] == {
        "Breakfast": 1200,
        "Midday": 1200,
        "Drive": 1500,
        "Night": 0,
    }
    assert report["problems"] == rejected