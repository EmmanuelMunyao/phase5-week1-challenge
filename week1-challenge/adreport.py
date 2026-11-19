import csv
import json
import sys
from pathlib import Path

from checks import check_rows
from summary import build_report, ranked


REQUIRED_COLUMNS = {
    "spot_id",
    "date",
    "time",
    "advertiser",
    "seconds",
}


def print_report(report: dict, output_path: Path) -> None:
    print(
        f"{report['station']}: advert report for "
        f"{report['source']}"
    )
    print(
        f"Spots aired {report['first_day']} "
        f"to {report['last_day']}"
    )
    print(
        f"Rows read: {report['rows_read']}, "
        f"accepted: {report['accepted']}, "
        f"rejected: {report['rejected']}"
    )

    print()
    print(
        f"{'Advertiser':<28}"
        f"{'Spots':>6}"
        f"{'Seconds':>10}"
        f"{'KSh':>10}"
    )

    for advertiser in report["advertisers"]:
        print(
            f"{advertiser['name']:<28}"
            f"{advertiser['spots']:>6}"
            f"{advertiser['seconds']:>10}"
            f"{advertiser['amount_ksh']:>10,}"
        )

    total_seconds = sum(
        advertiser["seconds"]
        for advertiser in report["advertisers"]
    )

    print(
        f"{'Total':<28}"
        f"{report['accepted']:>6}"
        f"{total_seconds:>10}"
        f"{report['total_ksh']:>10,}"
    )

    print()
    print(f"{'Slot':<44}{'KSh':>10}")

    for slot, amount in report["slots_ksh"].items():
        print(f"{slot:<44}{amount:>10,}")

    print()
    print("Rejected rows")

    for problem in report["problems"]:
        print(problem)

    print()
    print(f"Saved {output_path}")


def main(csv_path: Path) -> None:
    try:
        with open(
            csv_path,
            newline="",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)

            fieldnames = reader.fieldnames or []

            missing = sorted(
                REQUIRED_COLUMNS - set(fieldnames)
            )

            if missing:
                print(
                    f"{csv_path.name} is missing the column(s): "
                    f"{', '.join(missing)}"
                )
                return

            rows = list(reader)

    except FileNotFoundError:
        sys.exit(f"No such file: {csv_path}")

    spots, rejected = check_rows(rows)

    if not spots:
        sys.exit(
            f"No valid spots in {csv_path.name}: "
            "nothing to report."
        )

    report = build_report(
        csv_path.name,
        len(rows),
        spots,
        rejected,
    )

    reports_dir = Path(__file__).parent / "reports"
    reports_dir.mkdir(exist_ok=True)

    output_path = (
        reports_dir
        / f"{csv_path.stem}-report.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            report,
            file,
            indent=2,
        )

    print_report(report, output_path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 adreport.py PATH_TO_CSV")

    main(Path(sys.argv[1]))