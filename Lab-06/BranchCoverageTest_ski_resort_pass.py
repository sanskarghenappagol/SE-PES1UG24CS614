
import pytest

from ski_resort_pass import (
    process_resort_bookings,
    check_chairlift_anemometer,
)


def test_valid_and_invalid_inputs():
    with pytest.raises(ValueError):
        process_resort_bookings("invalid", 10)

    with pytest.raises(ValueError):
        process_resort_bookings([], -1)

    assert process_resort_bookings([], 10)["status"] == "ZERO_SALES"


def test_inactive_and_empty_groups():
    groups = [
        {"is_active": False},
        {"is_active": True, "duration": "full_day", "skiers": []},
    ]
    assert process_resort_bookings(groups, 10)["status"] == "ZERO_SALES"


def test_all_pass_durations():
    groups = [
        {"is_active": True, "duration": "season",
         "skiers": [{"age": 30}]},
        {"is_active": True, "duration": "full_day",
         "skiers": [{"age": 30}]},
        {"is_active": True, "duration": "half_day",
         "skiers": [{"age": 30}]},
    ]
    result = process_resort_bookings(groups, 0)
    assert result == {
        "total_revenue": 430.0,
        "status": "COMPLETED",
    }


def test_unknown_duration():
    groups = [{
        "is_active": True,
        "duration": "weekend",
        "skiers": [{"age": 30}],
    }]
    assert process_resort_bookings(groups, 0)["status"] == "ZERO_SALES"


def test_child_adult_and_senior_discounts():
    groups = [{
        "is_active": True,
        "duration": "full_day",
        "skiers": [
            {"age": 11},
            {"age": 12},
            {"age": 64},
            {"age": 65},
        ],
    }]
    assert process_resort_bookings(groups, 0)["total_revenue"] == 264.0


def test_invalid_age_and_audit_review():
    groups = [{
        "is_active": True,
        "duration": "full_day",
        "skiers": [{"age": 0} for _ in range(5)],
    }]
    assert process_resort_bookings(groups, 0) == {
        "total_revenue": 0.0,
        "status": "AUDIT_REVIEW",
    }


def test_gear_rental_and_lodge_locker():
    groups = [{
        "is_active": True,
        "duration": "full_day",
        "skiers": [
            {"age": 30, "gear_rental": True},
            {"age": 30, "gear_rental": False},
        ],
        "includes_lodge_locker": True,
    }]
    assert process_resort_bookings(groups, 15) == {
        "total_revenue": 210.0,
        "status": "COMPLETED",
    }


def test_blackout_override_full_day():
    groups = [{
        "is_active": True,
        "duration": "full_day",
        "skiers": [
            {"age": 30, "blackout_override": True},
            {"age": 30, "blackout_override": False},
        ],
    }]
    assert process_resort_bookings(groups, 0)["total_revenue"] == 120.0


def test_blackout_override_half_day_stops_group():
    groups = [{
        "is_active": True,
        "duration": "half_day",
        "skiers": [
            {"age": 30},
            {"age": 30, "blackout_override": True},
            {"age": 30},
        ],
    }]
    assert process_resort_bookings(groups, 0)["total_revenue"] == 0.0


def test_zero_sales_status():
    groups = [{
        "is_active": True,
        "duration": "full_day",
        "skiers": [{"age": 0}],
    }]
    assert process_resort_bookings(groups, 0)["status"] == "ZERO_SALES"


def test_no_wind_data():
    assert check_chairlift_anemometer([]) == "NO_DATA"


def test_empty_lift_readings():
    assert check_chairlift_anemometer([[], [20, 30]]) == "SAFE_OPERATION"


def test_safe_and_interrupted_gusts():
    assert check_chairlift_anemometer(
        [[46, 30, 47]]
    ) == "SAFE_OPERATION"


def test_two_consecutive_high_gusts():
    assert check_chairlift_anemometer(
        [[46, 47]]
    ) == "SUSPEND_LIFT"


def test_multiple_lifts():
    assert check_chairlift_anemometer(
        [[46], [20, 46, 47]]
    ) == "SUSPEND_LIFT"
