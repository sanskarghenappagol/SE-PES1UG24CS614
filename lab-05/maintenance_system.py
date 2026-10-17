"""Warehouse asset maintenance registry.

Registers machines, records service dates, raises alerts for overdue
inspections and exports a report to a JSON file.
"""
import json
import os
import tempfile
from datetime import datetime, timedelta

DATE_FORMAT = "%Y-%m-%d"

# Global state
assets = {}
registration_log = []
settings = {"service_interval_days": 90}


def register_asset(asset_id, machine_type, logs=None):
    """Register a new asset. Return True on success, False if rejected."""
    if logs is None:
        logs = registration_log
    asset_id = asset_id.strip()
    if not asset_id:
        print("Rejected: asset ID must not be empty")
        return False
    if asset_id in assets:
        print("Rejected:", asset_id, "is already registered")
        return False
    assets[asset_id] = {
        "type": machine_type,
        "last_service": datetime.now().strftime(DATE_FORMAT),
    }
    logs.append(asset_id)
    print("Registered", asset_id, "- total registrations this run:", len(logs))
    return True


def update_service_date(asset_id, date):
    """Set an asset's last service date. Return True on success."""
    if asset_id not in assets:
        print("Could not update", asset_id, "- asset not found")
        return False
    try:
        parsed = datetime.strptime(date, DATE_FORMAT)
    except ValueError:
        print("Could not update", asset_id, "- invalid date:", repr(date))
        return False
    if parsed > datetime.now():
        print("Could not update", asset_id, "- date is in the future")
        return False
    assets[asset_id]["last_service"] = date
    return True


def due_for_inspection():
    """Return the IDs of assets whose service interval has elapsed."""
    interval = timedelta(days=settings["service_interval_days"])
    due = []
    for asset_id, info in assets.items():
        last = datetime.strptime(info["last_service"], DATE_FORMAT)
        if datetime.now() - last > interval:
            due.append(asset_id)
    return due


def change_interval(days):
    """Change the service interval (must be a positive number of days)."""
    if days <= 0:
        print("Rejected: interval must be a positive number of days")
        return False
    settings["service_interval_days"] = days
    return True


def export_service_report(file="maintenance.json"):
    """Write all assets to a JSON report."""
    with open(file, "w", encoding="utf-8") as report:
        json.dump(assets, report, indent=2)
    print("Report written to " + file)


def write_scratch_copy():
    """Write a scratch copy of the assets to a secure temporary file."""
    file_descriptor, path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(file_descriptor, "w", encoding="utf-8") as scratch:
        json.dump(assets, scratch)
    print("Scratch copy at", path)


def print_alerts():
    """Print an alert for every asset that is overdue for inspection."""
    for asset_id in due_for_inspection():
        print("ALERT: inspection overdue for", asset_id,
              assets[asset_id]["type"])


def main():
    """Run the maintenance registry demo."""
    register_asset("FL-01", "Forklift")
    register_asset("CV-07", "Conveyor")
    register_asset("", "Pallet Jack")
    register_asset("FL-01", "Crane")
    update_service_date("FL-01", "2025-01-15")
    update_service_date("XX-99", "2025-02-01")
    change_interval(-30)
    date = input("Last service date for CV-07 (YYYY-MM-DD, Enter to skip): ")
    if date:
        update_service_date("CV-07", date)
    if not assets:
        print("No assets registered - nothing to report")
        return
    print_alerts()
    export_service_report()
    write_scratch_copy()


if __name__ == "__main__":

    main()
