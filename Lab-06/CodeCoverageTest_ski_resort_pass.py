
import pytest

from ski_resort_pass import (
    process_resort_bookings,
    check_chairlift_anemometer,
)


def test_invalid_groups():
    with pytest.raises(ValueError):
        process_resort_bookings("invalid", 10)


def test_negative_facility_fee():
    with pytest.raises(ValueError):
        process_resort_bookings([], -1)


def test_empty_groups():
    assert process_resort_bookings([], 10) == {
        "total_revenue": 0.0,
        "status": "ZERO_SALES",
    }


def test_inactive_group():
    assert process_resort_bookings(
        [{"is_active": False}], 10
    )["status"] == "ZERO_SALES"


def test_season_pass_with_gear_and_locker():
    groups = [{
        "is_active": True,
        "duration": "season",
        "skiers": [{"age": 30, "gear_rental": True}],
        "includes_lodge_locker": True,
    }]
    assert process_resort_bookings(groups, 20) == {
        "total_revenue": 355.0,
        "status": "COMPLETED",
    }


def test_full_day_child_and_senior():
    groups = [{
        "is_active": True,
        "duration": "full_day",
        "skiers": [{"age": 10}, {"age": 70}],
    }]
    assert process_resort_bookings(groups, 0)["total_revenue"] == 104.0


def test_half_day_blackout_override():
    groups = [{
        "is_active": True,
        "duration": "half_day",
        "skiers": [
            {"age": 30, "blackout_override": True},
            {"age": 25},
        ],
    }]
    assert process_resort_bookings(groups, 0)["total_revenue"] == 0.0


def test_full_day_blackout_override():
    groups = [{
        "is_active": True,
        "duration": "full_day",
        "skiers": [{"age": 30, "blackout_override": True}],
    }]
    assert process_resort_bookings(groups, 0)["total_revenue"] == 40.0


def test_unknown_duration():
    groups = [{
        "is_active": True,
        "duration": "weekend",
        "skiers": [{"age": 30}],
    }]
    assert process_resort_bookings(groups, 0)["status"] == "ZERO_SALES"


def test_invalid_age():
    groups = [{
        "is_active": True,
        "duration": "full_day",
        "skiers": [{"age": 0}],
    }]
    assert process_resort_bookings(groups, 0)["total_revenue"] == 0.0


def test_audit_review():
    groups = [{
        "is_active": True,
        "duration": "full_day",
        "skiers": [{"age": 0} for _ in range(5)],
    }]
    assert process_resort_bookings(groups, 0)["status"] == "AUDIT_REVIEW"


def test_no_wind_data():
    assert check_chairlift_anemometer([]) == "NO_DATA"


def test_safe_wind_readings():
    assert check_chairlift_anemometer([[20, 30, 40]]) == "SAFE_OPERATION"


def test_two_consecutive_high_gusts():
    assert check_chairlift_anemometer([[46, 47]]) == "SUSPEND_LIFT"


def test_high_gusts_interrupted_by_safe_reading():
    assert check_chairlift_anemometer([[46, 30, 47]]) == "SAFE_OPERATION"
