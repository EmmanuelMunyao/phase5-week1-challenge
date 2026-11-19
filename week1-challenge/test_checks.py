import pytest
from datetime import date, time

from checks import (
    check_rows,
    parse_day,
    parse_row,
    parse_seconds,
    parse_time,
    slot_for,
    spot_price,
)


def test_parse_day_returns_date():
    assert parse_day("2026-11-05") == date(2026, 11, 5)


def test_parse_day_rejects_invalid_date():
    with pytest.raises(
        ValueError,
        match="date must be a real date like 2026-11-05",
    ):
        parse_day("2026-11-31")


def test_parse_time_returns_time():
    assert parse_time("06:15") == time(6, 15)


def test_parse_time_rejects_invalid_time():
    with pytest.raises(
        ValueError,
        match="time must be HH:MM like 06:15",
    ):
        parse_time("25:10")


def test_parse_time_rejects_before_station_opens():
    with pytest.raises(
        ValueError,
        match="the station is off air at 04:45",
    ):
        parse_time("04:45")


def test_parse_seconds_returns_integer():
    assert parse_seconds("30") == 30


def test_parse_seconds_rejects_non_number():
    with pytest.raises(
        ValueError,
        match="seconds must be a whole number",
    ):
        parse_seconds("thirty")


def test_parse_seconds_rejects_unsupported_length():
    with pytest.raises(
        ValueError,
        match="seconds must be 15, 30, 45 or 60",
    ):
        parse_seconds("20")


@pytest.mark.parametrize(
    "aired, expected",
    [
        (time(5, 0), "Breakfast"),
        (time(9, 59), "Breakfast"),
        (time(10, 0), "Midday"),
        (time(14, 59), "Midday"),
        (time(15, 0), "Drive"),
        (time(18, 59), "Drive"),
        (time(19, 0), "Night"),
    ],
)
def test_slot_for_edges(aired, expected):
    assert slot_for(aired) == expected


def test_spot_price_calculates_correctly():
    assert spot_price("Drive", 45) == 1500


def test_parse_row_returns_checked_spot():
    row = {
        "spot_id": "NK-1101",
        "date": "2026-11-02",
        "time": "06:15",
        "advertiser": "Gitimene Agrovet",
        "seconds": "30",
    }

    assert parse_row(row) == {
        "spot_id": "NK-1101",
        "date": date(2026, 11, 2),
        "advertiser": "Gitimene Agrovet",
        "seconds": 30,
        "slot": "Breakfast",
        "amount": 1200,
    }


def test_parse_row_strips_advertiser():
    row = {
        "spot_id": "NK-1109",
        "date": "2026-11-05",
        "time": "16:45",
        "advertiser": " Kinoru Hardware ",
        "seconds": "30",
    }

    spot = parse_row(row)

    assert spot["advertiser"] == "Kinoru Hardware"


def test_check_rows_rejects_duplicate_spot_id():
    rows = [
        {
            "spot_id": "NK-1108",
            "date": "2026-11-04",
            "time": "08:05",
            "advertiser": "Nkubu Technical College",
            "seconds": "60",
        },
        {
            "spot_id": "NK-1108",
            "date": "2026-11-04",
            "time": "08:05",
            "advertiser": "Nkubu Technical College",
            "seconds": "60",
        },
    ]

    spots, problems = check_rows(rows)

    assert len(spots) == 1
    assert problems == [
        "line 3: spot_id NK-1108 is already on line 2"
    ]